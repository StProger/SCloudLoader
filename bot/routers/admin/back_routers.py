from aiogram import types, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.keyboards.inline.admin import admin_sub_add_choose_markup
from bot.service.misc.misc_admin import admin_menu, sub_main, get_active_subs

admin_router = Router()


@admin_router.callback_query(F.data.startswith("too_"), StateFilter("*"))
async def back_processing(call: types.CallbackQuery, state: FSMContext):
    to_ = call.data[4:]
    await call.message.delete()

    if to_ == "admin_menu":
        await state.clear()
        await admin_menu(call.message)

    elif to_ == "subs_menu":
        await state.clear()
        await sub_main(call.message)

    elif to_ == "subs_added_menu":
        await state.clear()
        await get_active_subs(call.message)

    elif to_ == "links_menu":
        await state.set_state("admin:link")

    elif to_ == "op_add_choise":
        await state.clear()
        await call.message.answer(
            text="Добавление на ОП:",
            reply_markup=admin_sub_add_choose_markup()
        )

    # назад к выбору поста
    elif to_ == "mail_post_ask":
        await state.set_state("admin:mail:post")

        await call.message.answer("Что вы хотите отправить? Отправьте готовый пост.")