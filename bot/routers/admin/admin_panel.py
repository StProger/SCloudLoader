from aiogram import types, Router, F

from bot.service.misc.misc_messages import admin_panel_main


router = Router()


@router.callback_query(F.data == "admin_panel")
async def admin_panel_handler(
        callback: types.CallbackQuery
):

    await admin_panel_main(callback)
