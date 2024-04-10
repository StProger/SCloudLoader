from bot.database.models.user import User

from aiogram import Bot, types


sub_inline = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="Подписка💸", callback_data="sub_user"
            )
        ]
    ]
)


async def notification_sub(bot: Bot):

    users: list[User] = await User.all()

    for user in users:

        if user.is_subscribed():

            expire_days = await user.expire_sub()

            if expire_days == 5:
                await bot.send_message(
                    chat_id=user.user_id,
                    text="❗️Подписка истекает через 5 дней❗️",
                    reply_markup=sub_inline
                )
            elif expire_days == 3:
                await bot.send_message(
                    chat_id=user.user_id,
                    text="❗️Подписка истекает через 3 дня❗️",
                    reply_markup=sub_inline
                )
            elif expire_days == 1:
                await bot.send_message(
                    chat_id=user.user_id,
                    text="❗️Подписка истекает через 1 день❗️",
                    reply_markup=sub_inline
                )


