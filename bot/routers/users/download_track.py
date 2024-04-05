from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from bot.database.models.user import User


router = Router()


@router.callback_query(
    F.data == "download_track"
)
async def get_link_track(
        callback: types.CallbackQuery,
        state: FSMContext,
        user: User
):
    """ Кнопка "Скачать трек" """

    if not (await user.is_subscribed()):

        await callback.answer("У вас нет подписки❌",
                              show_alert=True)
    else:
        return
