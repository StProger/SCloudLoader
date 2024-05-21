import sys
import os

from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from aiogram import Dispatcher, Bot

from bot.database.config import db, TORTOISE_CONFIG
from bot.database.models.user import User
from bot.settings import settings, BOT_SCHEDULER
from bot.middlewares import register_all_middlewares
from bot.routers import register_all_routers
from bot import logging
from bot.service.misc.notification_sub import notification_sub
from bot.bot_commands import set_bot_commands

import asyncio

from pyrogram import Client


async def main():

    if not(os.path.exists("bot/service/sound_cloud/tracks")):
        os.mkdir("bot/service/sound_cloud/tracks")
    storage = RedisStorage.from_url(settings.fsm_redis_url)

    dp = Dispatcher(storage=storage)

    bot = Bot(settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML", link_preview_is_disabled=True))

    client = Client(
        "bot",
        api_id=settings.API_ID,
        api_hash=settings.API_HASH,
        bot_token=settings.BOT_TOKEN
    )

    register_all_middlewares(dp)
    register_all_routers(dp)

    await set_bot_commands(bot)

    await logging.setup()

    BOT_SCHEDULER.add_job(notification_sub, trigger="interval", hours=24, args=(bot,))
    BOT_SCHEDULER.start()

    try:

        await db.init(TORTOISE_CONFIG)
        await client.start()
        await dp.start_polling(bot)

    except KeyboardInterrupt:
        sys.exit(1)
    finally:
        await bot.session.close()


if __name__ == '__main__':

    asyncio.run(main())
