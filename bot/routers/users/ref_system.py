from aiogram import types, F, Router, Bot

from bot.database.models.user import User

from bot.service.misc.misc_messages import referal_system


router = Router()


@router.callback_query(F.data == "ref_system")
async def ref_system_callback(
        callback: types.CallbackQuery,
        user: User
):

    await referal_system(callback, user)
