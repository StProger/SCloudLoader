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


def main_inline_admin():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Админ-панель🔐", callback_data="admin_panel"
                )
            ],
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


def sub_inline():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Crypto (CryptoCloud)", callback_data="crypto_pay_sub"
                ),
                InlineKeyboardButton(
                    text="Карта (Lava)", callback_data="card_pay_sub"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Меню", callback_data="menu"
                )
            ]
        ]
    )


def download_track_inline():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Меню", callback_data="menu"
                )
            ]
        ]
    )


def choose_crypto_inline():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="1 месяц", callback_data="month_crypto_1"
                ),
                InlineKeyboardButton(
                    text="3 месяца", callback_data="month_crypto_3"
                ),
                InlineKeyboardButton(
                    text="6 месяцев", callback_data="month_crypto_6"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад", callback_data="sub"
                ),
                InlineKeyboardButton(
                    text="Меню", callback_data="menu"
                )
            ]
        ]
    )


def choose_card_inline():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="1 месяц", callback_data="month_card_1"
                ),
                InlineKeyboardButton(
                    text="3 месяца", callback_data="month_card_3"
                ),
                InlineKeyboardButton(
                    text="6 месяцев", callback_data="month_card_6"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад", callback_data="sub"
                ),
                InlineKeyboardButton(
                    text="Меню", callback_data="menu"
                )
            ]
        ]
    )
