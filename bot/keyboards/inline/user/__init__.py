from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.sub import Sub


def not_subbed_markup(sponsors: list[Sub]):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            *[[
                InlineKeyboardButton(text="Запустите" if sub.is_bot else "Подпишитесь", url=sub.link)
            ] for sub in sponsors],
            [
                InlineKeyboardButton(text="🔄 Проверить подписку", callback_data="checksub")
            ]
        ]
    )


def main_inline():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Скачать музыку🎧", callback_data="download_track"
                ),
                InlineKeyboardButton(
                    text="Подписка💸", callback_data="sub"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Реферальная система", callback_data="ref_system"
                ),
                InlineKeyboardButton(
                    text="Тех. поддержка", url="https://t.me/babodoy"
                )
            ]
        ]
    )
