from aiogram import Bot
from aiogram.types import Message, CallbackQuery

from bot.keyboards.inline.user import main_inline
from bot.keyboards.inline.user import download_track_inline
from bot.service.redis_serv.user import set_msg_to_delete


async def main_menu(message: Message):

    await message.answer(
        text="Главное меню",
        reply_markup=main_inline()
    )


async def callback_main_menu(callback: CallbackQuery):

    await callback.message.edit_text(
        text="Главное меню",
        reply_markup=main_inline()
    )


async def download_track(
        callback: CallbackQuery
):

    await set_msg_to_delete(
        callback.from_user.id,
        (await callback.message.edit_text(
        text="Отправь мне ссылку трека 🔗 на SoundCloud 👇",
        reply_markup=download_track_inline()
    )).message_id
    )
