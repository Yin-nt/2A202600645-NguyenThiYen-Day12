import json
import logging
import signal
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
import uvicorn

from app.auth import verify_api_key
from app.config import settings
from app.cost_guard import check_budget, record_cost
from app.rate_limiter import check_rate_limit
from app.storage import append_history, get_history, redis_client
from utils.mock_llm import ask as llm_ask

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(message)s",
)
logger = logging.getLogger(__name__)
START_TIME = time.time()
INSTANCE_ID = f"agent-{uuid.uuid4().hex[:8]}"
_ready = False


def log_event(event: str, **fields):
    logger.info(json.dumps({"event": event, "instance": INSTANCE_ID, **fields}))


@asynccontextmanager
async def lifespan(_app: FastAPI):
    global _ready
    redis_client.ping()
    _ready = True
    log_event("startup")
    yield
    _ready = False
    log_event("shutdown")
    redis_client.close()


app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)
    user_id: str = Field(default="default", min_length=1, max_length=100)


@app.middleware("http")
async def request_logging(request: Request, call_next):
    started = time.time()
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    log_event(
        "request",
        method=request.method,
        path=request.url.path,
        status=response.status_code,
        duration_ms=round((time.time() - started) * 1000, 2),
    )
    return response


@app.get("/health")
def health():
    return {"status": "ok", "instance": INSTANCE_ID, "uptime": round(time.time() - START_TIME, 1)}


@app.get("/ready")
def ready():
    if not _ready:
        raise HTTPException(503, "Not ready")
    try:
        redis_client.ping()
    except Exception as exc:
        raise HTTPException(503, "Redis unavailable") from exc
    return {"status": "ready", "instance": INSTANCE_ID}


@app.post("/ask")
def ask(body: AskRequest, _api_key: str = Depends(verify_api_key)):
    check_rate_limit(body.user_id)
    estimated_cost = max(0.001, len(body.question.split()) * 0.00001)
    check_budget(body.user_id, estimated_cost)

    history = get_history(body.user_id)
    answer = llm_ask(body.question)
    append_history(body.user_id, "user", body.question)
    append_history(body.user_id, "assistant", answer)
    record_cost(body.user_id, estimated_cost)

    return {
        "question": body.question,
        "answer": answer,
        "previous_messages": len(history),
        "instance": INSTANCE_ID,
    }


def shutdown_handler(signum, _frame):
    global _ready
    _ready = False
    log_event("SIGTERM", signum=signum)


signal.signal(signal.SIGTERM, shutdown_handler)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.host, port=settings.port, timeout_graceful_shutdown=30)
