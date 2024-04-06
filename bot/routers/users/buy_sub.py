from aiogram import types, Router, F


router = Router()


@router.callback_query(
    F.data == "crypto_pay_sub"
)
async def callback_query_crypto_pay_sub(
        callbac
):
    ...