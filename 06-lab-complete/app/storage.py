import json

import redis

from app.config import settings

redis_client = redis.from_url(settings.redis_url, decode_responses=True)


def get_history(user_id: str) -> list[dict]:
    values = redis_client.lrange(f"history:{user_id}", 0, -1)
    return [json.loads(value) for value in values]


def append_history(user_id: str, role: str, content: str) -> None:
    key = f"history:{user_id}"
    with redis_client.pipeline() as pipe:
        pipe.rpush(key, json.dumps({"role": role, "content": content}))
        pipe.ltrim(key, -20, -1)
        pipe.expire(key, settings.history_ttl_seconds)
        pipe.execute()
