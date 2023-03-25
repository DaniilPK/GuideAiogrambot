import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from redis.asyncio import Redis

from bot.config import load_config
from bot.db import create_session_pool
from bot.handlers import router_register
from bot.inline import register_inline
from bot.language.translator import Translator
from bot.middleware.redismiddleware import RedisMiddleware
from bot.middleware.session import SessionPoolMiddleware
from bot.middleware.translate import TranslatorMiddleware

logger = logging.getLogger(__name__)


def register_global_middlewares(dp: Dispatcher, session,redis):
    dp.inline_query.outer_middleware.register(SessionPoolMiddleware(session))
    dp.inline_query.outer_middleware.register(RedisMiddleware(redis))
    dp.message.middleware.register(TranslatorMiddleware())


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")

    config = load_config(".env")

    r = Redis()

    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(storage=MemoryStorage())

    session = await create_session_pool(config.db, False)
    register_global_middlewares(dp, session,r)

    router_register(dp)
    register_inline(dp)

    await dp.start_polling(bot, translator=Translator())


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit, RuntimeError):
        logger.error("Бот був вимкнений!")
