from aiogram import Router, F, types

from bot.database.models.user import User
from bot.keyboards.inline.user import sub_inline


router = Router()


@router.callback_query(
    F.data == "sub"
)
async def sub_callback(
        callback: types.CallbackQuery,
        user: User
):

    if not (await user.is_subscribed()):

        await callback.message.edit_text(
            text="У вас нет подписки❌",
            reply_markup=sub_inline()
        )

    else:

        expire = await user.expire_sub()
        await callback.message.edit_text(
            text=f"Ваша подписка заканчивается через {expire} дней.",
            reply_markup=sub_inline()
        )
