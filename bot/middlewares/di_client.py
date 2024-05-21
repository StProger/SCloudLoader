import typing
from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from pyrogram import Client

from bot.settings import settings


# Передача Client в handler
class DIClient(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: typing.Union[Message, CallbackQuery],
                       data):

        client = Client(
            "client",
            api_id=settings.API_ID,
            bot_token=settings.BOT_TOKEN
        )

        data["client"] = client
        return await handler(event, data)
