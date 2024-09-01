import pickle
import aioredis
import logging


class RedisCache:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(self.redis_url)
        logging.info("Redis connected!")

    async def disconnect(self):
        if self.redis:
            await self.redis.close()
            logging.info("Redis disconnected!")

    async def get(self, key: int):
        data = await self.redis.get(key)
        if data:
            logging.info("Redis found total_price: %s", data)
            return data
        logging.info("Redis didnt found total_price: %s", data)
        return None
    
    async def set(self, key: int, value: int):
        await self.redis.set(key, value)
        await self.redis.expire(key, 15)
        logging.info("Redis set total_price: %s", value)

    async def delete(self, key: int):
        await self.redis.delete(key)
        logging.info("Redis delete total_price")


# Функция для зависимостей FastAPI
async def get_redis_helper():
    redis_helper = RedisCache(
        redis_url=f"redis://redis:6379/0"
    )
    await redis_helper.connect()
    try:
        yield redis_helper
    finally:
        await redis_helper.disconnect()