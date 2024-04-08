from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from bot.settings import settings


class IsAdmin(Filter):
    """
    Check if user is an admin
    """

    async def __call__(self, update: Message | CallbackQuery) -> bool:
        return update.from_user.id in settings.ADMIN_IDS
