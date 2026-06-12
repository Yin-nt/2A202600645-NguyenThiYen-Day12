from datetime import datetime, timezone

from fastapi import HTTPException

from app.config import settings
from app.storage import redis_client


def _key(user_id: str) -> str:
    month = datetime.now(timezone.utc).strftime("%Y-%m")
    return f"budget:{user_id}:{month}"


def check_budget(user_id: str, estimated_cost: float) -> None:
    current = float(redis_client.get(_key(user_id)) or 0)
    if current + estimated_cost > settings.monthly_budget_usd:
        raise HTTPException(402, "Monthly budget exceeded")


def record_cost(user_id: str, cost: float) -> None:
    key = _key(user_id)
    with redis_client.pipeline() as pipe:
        pipe.incrbyfloat(key, cost)
        pipe.expire(key, 32 * 24 * 3600)
        pipe.execute()
