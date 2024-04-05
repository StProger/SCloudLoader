from bot.routers.users import free_attempt
from bot.routers import start
from bot.routers.users import download_track
from bot.routers.users import sub

from bot.filters.free_attempt import FreeAttempts

from aiogram import F, Dispatcher


def register_all_routers(dp: Dispatcher):
    # Подключение фильтров

    free_attempt.router.message.filter(F.chat.type == "private")

    dp.include_router(free_attempt.router)
    dp.include_router(start.router)
    dp.include_router(download_track.router)
    dp.include_router(sub.router)
