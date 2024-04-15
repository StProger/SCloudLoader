from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def admin_menu_markup():
    """главное меню админа"""
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Включить подписку✅",
                        callback_data="switch_on_sub"
                    ),
                    InlineKeyboardButton(
                        text="Выключить подписку❌",
                        callback_data="switch_off_sub"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔐 Обяз. Подписка",
                        callback_data="sub"
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="📨 Рассылка",
                        callback_data="admin_mailing"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Меню",
                        callback_data="menu"
                    )
                ]
            ]
    )


def admin_mailing_confirm():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Да✅", callback_data=f"mailing_confirm"),
            ],
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data=f"too_admin_menu"),
            ]
        ]
    )


def admin_sub_markup():
    """обяз подписка у админа"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Добавить➕", callback_data="sub_add"),
                InlineKeyboardButton(text="Добавленные✔️", callback_data="sub_added"),

            ],
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="too_admin_menu"),
            ],
        ]
    )


def admin_sub_add_choose_markup():
    """выбор на ОП бот/канал"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Бота🤖", callback_data="op_bot"),
                InlineKeyboardButton(text="Канал🚪", callback_data="op_channel"),

            ],
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="too_subs_menu"),
            ],
        ]

    )


def admin_sub_add_confirm_markup():
    """подтверждение добавление ОП/канала """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅", callback_data="yes"),
                InlineKeyboardButton(text="❌", callback_data="no"),

            ]
        ]

    )


def admin_op_back_to_choose_b_c():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="too_op_add_choise"),
            ],
        ]

    )

def admin_sub_list_markup(subs: list[list[int, str, bool]]):
    builder = InlineKeyboardBuilder()

    for idx, s in enumerate(subs):
        if s[2]:
            subs[idx][2] = "🤖"
        else:
            subs[idx][2] = "🚪"

    [
        builder.button(
            text=s[2] + s[1],
            callback_data=f"checksub_{s[0]}"
        ) for s in subs]

    builder.button(
        text="🔙 Назад", callback_data="too_subs_menu"
    )

    builder.adjust(1)

    return builder.as_markup()


def admin_del_sub(sub_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🗑 Удалить ОП", callback_data=f"delsub_{sub_id}"),

            ],
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="too_subs_added_menu")
            ]
        ]

    )

