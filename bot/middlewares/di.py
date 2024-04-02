import html
import typing
from typing import Callable, Dict, Awaitable, Any

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from bot.database.models.user import User


# Проверка юзера в БД и его добавление
class ExistsUserMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: typing.Union[Message, CallbackQuery],
                       data):

        this_user = data.get("event_from_user")

        if not this_user.is_bot:
            get_user: User = await User.get_or_none(user_id=this_user.id)

            user_id = this_user.id
            username = this_user.username
            first_name = this_user.first_name
            last_name = this_user.last_name
            full_name = this_user.first_name
            language_code = this_user.language_code

            if username is None: username = ""
            if first_name is None: first_name = ""
            if last_name is None: last_name = ""
            if full_name is None: full_name = ""
            if language_code != "ru": language_code = "en"

            if len(last_name) >= 1: full_name += f" {last_name}"

            if get_user is None:

                get_user: User = await User.create(
                    user_id=user_id,
                    username=username.lower(),
                    first_name=html.escape(first_name),
                    last_name=html.escape(last_name),
                    full_name=html.escape(full_name),
                    language_code=language_code
                )

            else:
                if first_name != get_user.first_name:
                    await get_user.update_from_dict({"first_name": first_name}).save()

                if last_name != get_user.last_name:
                    await get_user.update_from_dict({"last_name": last_name}).save()

                if full_name != get_user.full_name:
                    await get_user.update_from_dict({"full_name": full_name}).save()

                if username.lower() != get_user.username:
                    await get_user.update_from_dict({"useranme": username}).save()

            data['user'] = await (User.filter(user_id=user_id)
                                  .first()
                                  )

        return await handler(event, data)
