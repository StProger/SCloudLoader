import typing

from aiogram import types, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.database.models.sub import Sub
from bot.keyboards.inline.admin import admin_sub_add_choose_markup, admin_sub_add_confirm_markup, \
    admin_op_back_to_choose_b_c
from bot.service.misc.misc_admin import check_token_valid, admin_menu, sub_main, get_active_subs, sub_info

admin_router = Router()


@admin_router.callback_query(F.data == "sub")
async def profile_refill_initiate(call: types.CallbackQuery):
    await call.answer()
    await call.message.delete()
    await sub_main(call.message)


@admin_router.callback_query(F.data.startswith("sub_"))
async def sub_actions(call: types.CallbackQuery):
    await call.answer()
    await call.message.delete()

    action_: str = call.data.split("_")[1]

    if action_ == "add":
        await call.message.answer(
            text="Добавление на ОП:",
            reply_markup=admin_sub_add_choose_markup()
        )

    elif action_ == "added":
        await get_active_subs(call.message)


@admin_router.callback_query(F.data.startswith("op_"))
async def op_add_choice(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()

    type_: str = call.data.split("_")[1]

    is_bot: bool = type_ == "bot"

    await state.set_state("op:type")
    await state.update_data(
        is_bot=is_bot
    )

    await state.set_state("op:data")

    await call.message.answer(f"""
Введите данные в формате:
<code>
  {'Токен бота *' if is_bot else 'ID канала'}
  Название кнопки (идентификатор для админки)
  {'Ссылка на бота' if is_bot else  'Ссылка на канал'}
</code>

{'НУЖНО ДОБАВИТЬ НАШЕГО БОТА В АДМИНЫ ЭТОГО КАНАЛА' if ~is_bot else ''}
""", reply_markup=admin_op_back_to_choose_b_c())


@admin_router.message(StateFilter("op:data"))
async def op_add_data(message: types.Message, state: FSMContext):
    data = message.text

    if len(data.split("\n")) != 3:
        return await message.answer("Данные введены неверно! Должно быть 3 строки. Введите ещё раз.")

    data = [d.strip() for d in data.split("\n")]

    bot_token, title, link = data

    is_bot = (await state.get_data())['is_bot']

    if is_bot and not await check_token_valid(bot_token, message.bot.session):
        return await message.answer("Токен бота невалид. Введите ещё раз.")

    await state.update_data(
        bot_token=str(bot_token).replace("-100", ""),
        title=title,
        link=link
    )
    await state.set_state("op:confirm")

    await message.answer(
        text=f"""
Данные по ОП

Ресурс: {'🤖' if is_bot else '🚪'}
{'Токен бота' if is_bot else 'ID канала'}: <code>{str(bot_token).replace("-100", "")}</code>
Название кнопки: <code>{title}</code>
Ссылка: <code>{link}</code>

Подтверждаете добавление?
""",
        reply_markup=admin_sub_add_confirm_markup()
    )


@admin_router.callback_query(StateFilter("op:confirm"))
async def op_add_data(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()

    if call.data == "yes":
        data = await state.get_data()
        await Sub.create(**data)
        await call.message.answer("ОП успешно добавлено!")

    elif call.data == "no":
        await call.message.answer("Добавление прекращено!")

    await admin_menu(call.message)
    await state.clear()


@admin_router.callback_query(F.data.startswith("checksub_"))
async def op_get_info(call: types.CallbackQuery):
    """инфо по оп и удаление"""
    await call.answer()
    await call.message.delete()

    await sub_info(call.message, int(call.data.split("_")[1]))


@admin_router.callback_query(F.data.startswith("delsub_"))
async def op_get_info(call: types.CallbackQuery):
    """удалене ОП"""
    await call.answer()
    await call.message.delete()

    await Sub.filter(id=call.data.split("_")[1]).delete()

    await call.message.answer("ОП удалено.")
    await sub_main(call.message)