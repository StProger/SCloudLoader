from aiogram import Router, types, F
from aiogram.filters import StateFilter
from aiogram.filters.command import Command

from bot.settings import settings


router = Router()


@router.message(StateFilter("*"), Command("term"))
async def term_handler(message: types.Message):

    await message.answer(
        text="👇",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="Публичная оферта", url=settings.public_offer
                    )
                ],
                [
                    types.InlineKeyboardButton(
                        text="Обработка персональных данных", url=settings.personal_data
                    )
                ]
            ]
        )
    )
