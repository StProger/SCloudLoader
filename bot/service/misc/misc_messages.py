from aiogram import Bot
from aiogram.types import Message, CallbackQuery

from bot.keyboards.inline.user import main_inline


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
