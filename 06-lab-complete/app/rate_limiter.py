import time
import uuid

from fastapi import HTTPException

from app.config import settings
from app.storage import redis_client


def check_rate_limit(user_id: str) -> None:
    now = time.time()
    key = f"rate:{user_id}"
    with redis_client.pipeline() as pipe:
        pipe.zremrangebyscore(key, 0, now - 60)
        pipe.zcard(key)
        pipe.zadd(key, {f"{now}:{uuid.uuid4().hex}": now})
        pipe.expire(key, 60)
        _, count, _, _ = pipe.execute()
    if count >= settings.rate_limit_per_minute:
        redis_client.zremrangebyscore(key, now, now)
        raise HTTPException(429, "Rate limit exceeded", headers={"Retry-After": "60"})
