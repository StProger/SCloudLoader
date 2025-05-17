from aiogram import types, Router, F
from aiogram.types import PreCheckoutQuery

from bot.service.misc.misc_messages import stars_menu, create_invoice_stars_pay, successful_payment_stars

from bot.database.models.user import User


router = Router()


@router.callback_query(F.data == "stars_pay_sub")
async def callback_query_crypto_pay_sub(
        callback: types.CallbackQuery
):

    await stars_menu(callback=callback)


@router.callback_query(
    F.data.contains("month_stars_")
)
async def create_invoice_(
        callback: types.CallbackQuery,
        user: User
):
    await callback.message.delete()
    await create_invoice_stars_pay(
        callback=callback,
        user=user
    )


@router.pre_checkout_query()
async def on_pre_checkout_query(
    pre_checkout_query: PreCheckoutQuery,
):
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def on_successful_payment(
    message: types.Message,
    user: User
):
    payload = message.successful_payment.invoice_payload

    await successful_payment_stars(user=user, order_id=int(payload), message=message)