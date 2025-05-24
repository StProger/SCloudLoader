from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.models.sub import Sub
from bot.settings import settings


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


def main_inline() -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Скачать музыку🎧", callback_data="download_track"
                ),
                InlineKeyboardButton(
                    text="Подписка💸", callback_data="sub_user"
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
                    text="Подписка💸", callback_data="sub_user"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Реферальная система", callback_data="ref_system"
                ),
                InlineKeyboardButton(
                    text="Тех. поддержка", url="@vzavyazkebot"
                )
            ]
        ]
    )


def sub_inline():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                # InlineKeyboardButton(
                #     text="Crypto (CryptoCloud)", callback_data="crypto_pay_sub"
                # ),
                InlineKeyboardButton(
                    text='Звёзды 🌟', callback_data="stars_pay_sub"
                )
                # InlineKeyboardButton(
                #     text="Карта (Lava)", callback_data="card_pay_sub"
                # )
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
            ],
            [
                InlineKeyboardButton(
                    text="Как получить ссылку", url="https://telegra.ph/Poluchenie-ssylki-na-trek-SoundCloud-04-15"
                )
            ]
        ]
    )


def choose_crypto_inline():
    PRICES = settings.PRICES
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"1 месяц - {PRICES['crypto'][1]['price']}₽", callback_data="month_crypto_1"
                ),
                InlineKeyboardButton(
                    text=f"3 месяца - {PRICES['crypto'][3]['price']}₽", callback_data="month_crypto_3"
                ),
                InlineKeyboardButton(
                    text=f"12 месяцев - {PRICES['crypto'][12]['price']}₽", callback_data="month_crypto_12"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад", callback_data="sub_user"
                ),
                InlineKeyboardButton(
                    text="Меню", callback_data="menu"
                )
            ]
        ]
    )


def choose_card_inline():

    PRICES = settings.PRICES
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"1 месяц - {PRICES['card'][1]['price']}₽", callback_data="month_card_1"
                ),
                InlineKeyboardButton(
                    text=f"3 месяца - {PRICES['card'][3]['price']}₽", callback_data="month_card_3"
                ),
                InlineKeyboardButton(
                    text=f"12 месяцев - {PRICES['card'][12]['price']}₽", callback_data="month_card_12"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад", callback_data="sub_user"
                ),
                InlineKeyboardButton(
                    text="Меню", callback_data="menu"
                )
            ]
        ]
    )


def choose_stars_inline():

    PRICES = settings.PRICES
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"1 месяц - {PRICES['stars'][1]['price']}🌟", callback_data="month_stars_1"
                ),
                InlineKeyboardButton(
                    text=f"3 месяца - {PRICES['stars'][3]['price']}🌟", callback_data="month_stars_3"
                ),
                InlineKeyboardButton(
                    text=f"12 месяцев - {PRICES['stars'][12]['price']}🌟", callback_data="month_stars_12"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад", callback_data="sub_user"
                ),
                InlineKeyboardButton(
                    text="Меню", callback_data="menu"
                )
            ]
        ]
    )


def main_menu_key():

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Меню", callback_data="menu"
                )
            ]
        ]
    )