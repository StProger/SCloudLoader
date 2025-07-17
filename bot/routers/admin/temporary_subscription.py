from datetime import timedelta

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.database.models.user import User
from bot.keyboards.inline.admin import admin_temporary_sub

router = Router()

@router.callback_query(F.data == "temporary_subscription")
async def insert_user_id(callback: types.CallbackQuery, state: FSMContext):

    await callback.message.delete()
    await state.set_state("temporary_subscription:get_user_id")
    await callback.message.answer(
        text="<b>ID пользователя:</b>",
        reply_markup=admin_temporary_sub()
    )


@router.message(StateFilter("temporary_subscription:get_user_id"))
async def insert_days(message: types.Message, state: FSMContext):

    user_id = message.text
    try:
        user_id = int(user_id)
    except ValueError:
        await message.answer(
            text='Введён невалидный ID',
            reply_markup=admin_temporary_sub()
        )
        return
    user: User | None = await User.get_or_none(user_id=user_id)
    if not user:
        await message.answer(
            text="Нет такого пользователя в базе данных.",
            reply_markup=admin_temporary_sub()
        )
        return
    else:
        await state.set_state("temporary_subscription:get_sub_time")
        await state.update_data(user_id=user_id)
        await message.answer(
            text="<b>На сколько дней выдать подписку:</b>",
            reply_markup=admin_temporary_sub()
        )


@router.message(StateFilter("temporary_subscription:get_sub_time"))
async def give_suv(message: types.Message, state: FSMContext):

    try:
        days = int(message.text)
    except ValueError:
        await message.answer(
            text="Введите число.",
            reply_markup=admin_temporary_sub()
        )
        return
    state_data = await state.get_data()
    user_id = state_data["user_id"]
    user: User | None = await User.get_or_none(user_id=user_id)

    if user:
        user.subscription_to = (user.subscription_to + timedelta(days=days))
        await user.save()
        await state.clear()
        await message.answer(
            text=f"Подписка пользователю с ID {user_id} выдана на {days} дней.",
            reply_markup=admin_temporary_sub()
        )
    else:
        await message.answer(text="Нет такого пользователя с базе данных.",
                             reply_markup=admin_temporary_sub())