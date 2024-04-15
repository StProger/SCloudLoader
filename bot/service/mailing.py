import asyncio

from typing import Optional

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError, TelegramRetryAfter

from bot.database.models.user import User


async def start_mailing(
            message_id: int,
            reply_markup: Optional[dict],
            chat_id: int,
            bot: Bot
):

    delay = 1 / 25

    scope = await User.all()

    blocked = 0

    message = await bot.send_message(
        chat_id=chat_id,
        text="Рассылка запущена⏳"
    )

    for user in scope:

        try:

            await bot.copy_message(
                chat_id=user.user_id,
                from_chat_id=chat_id,
                message_id=message_id,
                reply_markup=reply_markup,
            )

        except TelegramRetryAfter as exc:

            delay *= 2
            await asyncio.sleep(exc.retry_after)

        except TelegramAPIError:

            blocked += 1

        await asyncio.sleep(delay)

    await message.answer(
        text="Рассылка завершена✅"
    )
