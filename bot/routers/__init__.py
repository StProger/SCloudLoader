from bot.routers.users import free_attempt

from bot.filters.free_attempt import FreeAttempts

from aiogram import F, Dispatcher


def register_all_routers(dp: Dispatcher):
    # Подключение фильтров

    free_attempt.router.message.filter(F.chat.type == "private")

    dp.include_router(free_attempt.router)
