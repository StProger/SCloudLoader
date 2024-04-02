import datetime
import time
import aiohttp

# from bot.service.redis_serv.user import get_time_of_sub_check, set_time_of_sub_check
from bot.settings import settings
from bot.database.models.user import User
from bot.database.models.sub import Sub

from contextlib import suppress
from typing import Any, Awaitable, Callable, Dict, Optional

from aiogram import BaseMiddleware, Bot
from aiogram.types import Update, Chat, Message
from aiogram.exceptions import (
    TelegramNotFound,
    TelegramForbiddenError,
    TelegramBadRequest, TelegramAPIError,
)
from aiogram.fsm.context import FSMContext


class SubMiddleware(BaseMiddleware):
    """
    Middleware for checking user's subscription
    """

    def __init__(self):

        self.session = aiohttp.ClientSession()

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any],
    ) -> Any:

        # if isinstance(event, Message) and event.text and "/start" in event.text:
        #     return await handler(event, data)

        user: Optional[User] = data.get('user')
        state: FSMContext = data['state']

        chat: Optional[Chat] = data.get('event_chat')

        # пропускаем админов без оп
        if not chat or user.user_id in settings.ADMIN_IDS:
            return await handler(event, data)

        # time_user_checked = await get_time_of_sub_check(user.user_id) or 0
        # time_to_check: bool = float(time_user_checked) < (datetime.datetime.now().timestamp() - 60)
        #
        # if (not time_to_check or chat.type != 'private' or await user.is_vip()) and user.subbed:
        #     return await handler(event, data)
        #
        # await set_time_of_sub_check(user.user_id)

        user = user or data.get('event_from_user')

        sponsors = await Sub.filter(is_active=True).all()

        available_sponsors = await self.get_sponsors(sponsors, user, data['bot'])

        # if not available_sponsors:
        #
        #     await state.update_data(
        #         last_check=time.time(),
        #     )

        data['sponsors'] = available_sponsors

        return await handler(event, data)

    async def get_sponsors(self, sponsors: list[Sub], user: User, bot: Bot) -> list[Sub]:

        response = [
                await self._check_sub(sponsor, user, bot)
                for sponsor in [
                    obj for obj in sponsors
                ]
        ]

        print(response)

        not_subbed = [
            sponsor for sponsor in response
            if sponsor is not None
        ]

        if bool(not_subbed):

            return not_subbed

        return []

    async def _check_sub(self, sponsor: Sub, user: User, bot: Bot) -> Optional[Sub]:
        print("here")
        if sponsor.is_bot:

            try:

                bot_ = Bot(sponsor.bot_token, session=bot.session)
                await bot_.send_chat_action(user.user_id, 'typing')

            except (
                TelegramNotFound,
                TelegramBadRequest,
                TelegramForbiddenError,
            ):

                return sponsor

        else:
            with suppress(TelegramAPIError):
                member = await bot.get_chat_member(
                    int("-100" + sponsor.bot_token),
                    user.user_id,
                )

                if member.status in ('left', 'kicked', None):

                    return sponsor