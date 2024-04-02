from aiogram.filters import Filter

from bot.database.models.user import User


class FreeAttempts(Filter):
    """
    Check if user have free attempts for download
    """

    async def __call__(self, _, user: User) -> bool:
        return bool(user.free_attempts < 2)
