from aiogram import types, Router, F

from bot.database.models.user import User
from bot.service.misc.misc_messages import crypto_menu
from bot.service.misc.misc_messages import create_invoice_crypto_pay


router = Router()


@router.callback_query(F.data == "crypto_pay_sub")
async def callback_query_crypto_pay_sub(
        callback: types.CallbackQuery
):

    await crypto_menu(callback=callback)


@router.callback_query(F.data.contains("month_crypto"))
async def create_invoice_(
        callback: types.CallbackQuery,
        user: User
):

    await create_invoice_crypto_pay(
        callback=callback,
        user=user
    )
