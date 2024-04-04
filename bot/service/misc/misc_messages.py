from aiogram import Bot
from aiogram.types import Message

from bot.keyboards.inline.user import main_inline


async def main_menu(message: Message):

    await message.answer(
        text="Главное меню",
        reply_markup=main_inline()
    )
