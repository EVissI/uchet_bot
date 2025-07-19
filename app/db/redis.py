import redis.asyncio as redis
from typing import Optional, List, Tuple

class RedisClient:
    def __init__(self, url: str = "redis://redis:6379/0"):
        self.url = url
        self.redis: Optional[redis.Redis] = None

    async def connect(self):
        self.redis = await redis.from_url(self.url, decode_responses=True)

    async def close(self):
        if self.redis:
            await self.redis.close()

    async def set(self, key: str, value: str, expire: int = None):
        await self.redis.set(key, value, ex=expire)

    async def get(self, key: str):
        return await self.redis.get(key)
    
    async def add_admin_message(self, user_id: int, admin_id: int, message_id: int):
        """
        Добавить сообщение админа для конкретного пользователя.
        Хранится как список строк "admin_id:message_id" по ключу f"admin_msgs:{user_id}"
        """
        key = f"admin_msgs:{user_id}"
        value = f"{admin_id}:{message_id}"
        await self.redis.rpush(key, value)

    async def get_admin_messages(self, user_id: int) -> List[Tuple[int, int]]:
        """
        Получить список (admin_id, message_id) для пользователя.
        """
        key = f"admin_msgs:{user_id}"
        values = await self.redis.lrange(key, 0, -1)
        result = []
        for v in values:
            try:
                admin_id, message_id = map(int, v.split(":"))
                result.append((admin_id, message_id))
            except Exception:
                continue
        return result

    async def clear_admin_messages(self, user_id: int):
        """
        Удалить все сообщения админов для пользователя.
        """
        key = f"admin_msgs:{user_id}"
        await self.redis.delete(key)

redis_client = RedisClient()