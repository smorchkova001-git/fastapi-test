from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from src.core.config import REDIS_HOST, REDIS_PORT

async def init_cache():
    redis_url = f"redis://{REDIS_HOST}:{REDIS_PORT}"
    print(f"🔄 Connecting to Redis at {redis_url}")
    redis = aioredis.from_url(redis_url)
    # Проверим подключение
    try:
        await redis.ping()
        print("✅ Redis ping successful")
    except Exception as e:
        print(f"❌ Redis ping failed: {e}")
        raise
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    print("✅ FastAPICache initialized")