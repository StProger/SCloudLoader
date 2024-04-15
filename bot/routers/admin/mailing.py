from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline.admin import admin_mailing_confirm

from bot.service.mailing import start_mailing

import asyncio


router = Router()


@router.callback_query(StateFilter("*"), F.data == "admin_mailing")
async def mailing_main(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state("admin:mailing:post")

    await callback.message.edit_text(
        text="Что вы хотите отправить? Отправьте готовый пост.",
        reply_markup=types.InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    types.InlineKeyboardButton(
                        text="🔙Назад", callback_data="too_admin_menu"
                    )
                ]
            ]
        )
    )


@router.message(StateFilter("admin:mailing:post"))
async def main_choose_post(message: types.Message, state: FSMContext):

    await state.update_data(message_id=message.message_id,
                            reply_markup=(
                                message.reply_markup.dict()
                                if message.reply_markup else None
                            ))

    await message.copy_to(
        message.from_user.id,
        reply_markup=message.reply_markup,
    )
    await message.answer(
        f"""
☝️Вот так выглядит ваш пост.

Запустить рассылку?""",
        reply_markup=admin_mailing_confirm()
    )

    await state.set_state("admin:mail:confirm")


@router.callback_query(StateFilter("admin:mail:confirm"))
async def admin_mail_confirm(callback: types.CallbackQuery, state: FSMContext):

    data = await state.get_data()

    asyncio.create_task(start_mailing(
        data["message_id"], data["reply_markup"],
        callback.message.chat.id, callback.message.bot
    ))
    await state.clear()
    await callback.answer()
