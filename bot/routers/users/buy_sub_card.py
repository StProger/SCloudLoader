from aiogram import types, Router, F

from bot.service.misc.misc_messages import card_menu
from bot.service.misc.misc_messages import create_invoice_card_pay

from bot.database.models.user import User



router = Router()


@router.callback_query(F.data == "card_pay_sub")
async def callback_query_crypto_pay_sub(
        callback: types.CallbackQuery
):

    await card_menu(callback=callback)


@router.callback_query(
    F.data.contains("month_card_")
)
async def create_invoice_(
        callback: types.CallbackQuery,
        user: User
):

    await create_invoice_card_pay(
        callback=callback,
        user=user
    )