from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import InlineQuery


class RedisMiddleware(BaseMiddleware):
    def __init__(self, redis) -> None:
        self.redis = redis

    async def __call__(
            self,
            handler: Callable[[InlineQuery, Dict[str, Any]], Awaitable[Any]],
            event: InlineQuery,
            data: Dict[str, Any]
    ) -> Any:
        data['redis'] = self.redis
        return await handler(event, data)
