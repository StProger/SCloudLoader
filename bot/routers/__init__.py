from bot.routers.users import free_attempt
from bot.routers import start
from bot.routers.users import download_track
from bot.routers.users import sub
from bot.routers.users import buy_sub_crypto
from bot.routers.users import buy_sub_card
from bot.routers.users import ref_system
from bot.routers.admin import expire_sub
from bot.routers.admin import switch_sub
from bot.routers.admin import admin_panel
from bot.routers.admin import back_routers
from bot.routers.admin.sub import admin_router as sub_admin
from bot.routers.admin import mailing
from bot.routers.users import terms

from bot.filters.free_attempt import FreeAttempts

from aiogram import F, Dispatcher


def register_all_routers(dp: Dispatcher):
    # Подключение фильтров

    free_attempt.router.message.filter(F.chat.type == "private")

    dp.include_router(free_attempt.router)
    dp.include_router(start.router)
    dp.include_router(download_track.router)
    dp.include_router(sub.router)
    dp.include_router(buy_sub_crypto.router)
    dp.include_router(buy_sub_card.router)
    dp.include_router(ref_system.router)
    dp.include_router(expire_sub.router)
    dp.include_router(switch_sub.router)
    dp.include_router(admin_panel.router)
    dp.include_router(sub_admin)
    dp.include_router(back_routers.admin_router)
    dp.include_router(mailing.router)
    dp.include_router(terms.router)
