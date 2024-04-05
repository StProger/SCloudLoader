import sys

from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram import Dispatcher, Bot

from bot.database.config import db, TORTOISE_CONFIG
from bot.settings import settings
from bot.middlewares import register_all_middlewares
from bot.routers import register_all_routers
from bot import logging

import asyncio


async def main():

    storage = RedisStorage.from_url(settings.fsm_redis_url)

    dp = Dispatcher(storage=storage)

    bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML", link_preview_is_disabled=True))

    register_all_middlewares(dp)
    register_all_routers(dp)

    await logging.setup()

    try:

        await db.init(TORTOISE_CONFIG)
        await dp.start_polling(bot)

    except KeyboardInterrupt:
        sys.exit(1)
    finally:
        await bot.session.close()


if __name__ == '__main__':

    asyncio.run(main())
