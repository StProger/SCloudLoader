from .di import ExistsUserMiddleware
from .subscription import SubMiddleware
from .throttling import ThrottlingMiddleware

from aiogram import Dispatcher

from bot.routers.users import free_attempt


# Регистрация всех мидлварей
def register_all_middlewares(dp: Dispatcher):

    dp.message.outer_middleware(ExistsUserMiddleware())
    dp.callback_query.outer_middleware(ExistsUserMiddleware())

    free_attempt.router.message.outer_middleware(SubMiddleware())
    free_attempt.router.callback_query.outer_middleware(SubMiddleware())

    dp.message.middleware(ThrottlingMiddleware())
