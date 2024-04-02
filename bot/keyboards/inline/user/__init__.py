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