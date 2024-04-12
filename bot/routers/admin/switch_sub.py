from datetime import timedelta

from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.database.models.user import User

from bot.service.misc.misc_messages import admin_panel_main
from bot.service.redis_serv.user import set_msg_to_delete, get_msg_to_delete


router = Router()

cancel_inline = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="Отмена❌", callback_data="cancel"
            )
        ]
    ]
)

menu_inline = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(
                text="Меню", callback_data="menu"
            )
        ]
    ]
)


@router.callback_query(
    StateFilter("*"),
    F.data == "cancel"
)
async def cancel(
        callback: types.CallbackQuery,
        state: FSMContext
):
    await state.clear()
    await admin_panel_main(callback)


@router.callback_query(F.data == "switch_on_sub")
async def get_username_user(
        callback: types.CallbackQuery,
        state: FSMContext
):

    await state.set_state("switch_on_sub:username")
    await set_msg_to_delete(callback.from_user.id,
                            (await callback.message.edit_text(
                                text="Отправьте username юзера",
                                reply_markup=cancel_inline
                            )).message_id)


@router.message(StateFilter("switch_on_sub:username"))
async def switch_on_sub(
        message: types.Message,
        state: FSMContext
):

    username = message.text.replace("@", "").replace("https://t.me/", "")

    user: User = await User.get_or_none(username=username)

    try:

        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=(await get_msg_to_delete(message.from_user.id))
        )
    except:
        pass
    await message.delete()
    if not user:

        await message.answer(
            text="Нет такого юзера❌",
            reply_markup=menu_inline
        )

    else:

        user.subscription_to = (user.subscription_to + timedelta(weeks=51))
        await user.save()
        await state.clear()
        await message.answer(
            text="Подписка включена✅",
            reply_markup=menu_inline
        )


@router.callback_query(F.data == "switch_off_sub")
async def get_username_user(
        callback: types.CallbackQuery,
        state: FSMContext
):

    await state.set_state("switch_off_sub:username")
    await set_msg_to_delete(callback.from_user.id,
                            (await callback.message.edit_text(
                                text="Отправьте @username юзера",
                                reply_markup=cancel_inline
                            )).message_id)


@router.message(StateFilter("switch_off_sub:username"))
async def switch_on_sub(
        message: types.Message,
        state: FSMContext
):

    username = message.text.replace("@", "").replace("https://t.me/", "")
    user: User = await User.get_or_none(username=username)

    try:

        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=(await get_msg_to_delete(message.from_user.id))
        )
    except:
        pass
    await message.delete()
    if not user:

        await message.answer(
            text="Нет такого юзера❌",
            reply_markup=menu_inline
        )

    else:

        user.subscription_to = (user.subscription_to - timedelta(weeks=51))
        await user.save()
        await state.clear()
        await message.answer(
            text="Подписка выключена✅",
            reply_markup=menu_inline
        )