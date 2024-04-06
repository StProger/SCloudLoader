from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext

from bot.service.misc.misc_messages import crypto_menu

router = Router()


@router.callback_query(
    F.data == "crypto_pay_sub"
)
async def callback_query_crypto_pay_sub(
        callback: types.CallbackQuery,
        state: FSMContext
):

    await crypto_menu(callback=callback)
