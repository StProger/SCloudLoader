from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, types, exceptions

from bot.filters.free_attempt import FreeAttempts
from bot.database.models.sub import Sub
from bot.database.models.user import User
from bot.keyboards.inline.user import not_subbed_markup
from bot.service.redis_serv.user import get_msg_to_delete, set_msg_to_delete


router = Router()

NOT_SUBBED = """
Подпишитесь на наши каналы!
"""


@router.message(FreeAttempts())
async def free_attempts(
        message: types.Message,
        state: FSMContext
):

    await set_msg_to_delete(message.from_user.id,
                            (await message.answer(
                                text="Отправь мне ссылку трека 🔗 на SoundCloud 👇"
                            )
                             ).message_id
                            )

    await state.set_state("free_attempts:link")


@router.message(StateFilter("free_attempts:link"))
async def download_music(
        message: types.Message,
        sponsors: list[Sub],
        state: FSMContext,
        user: User
):

    try:
        await message.bot.delete_message(
            message.from_user.id,
            (await get_msg_to_delete(
                user_id=message.from_user.id
            ))
        )
    except:
        pass

    await set_msg_to_delete(message.from_user.id,
                            message.message_id)

    if bool(sponsors):

        try:
            await message.answer(
                text=NOT_SUBBED,
                reply_markup=not_subbed_markup(sponsors)
            )
        except exceptions.TelegramAPIError:
            pass

        if user.subbed:
            user.subbed = False
            await user.save()

        await state.clear()

    else:

        # Тут логика скачивания музыки и отправка
        ...


@router.callback_query(F.data == "checksub")
async def subbed(callback: types.CallbackQuery,
                 user: User,
                 sponsors: list[Sub],
                 state: FSMContext):

    if bool(sponsors):

        await callback.answer("Вы не подписались❌")
    else:
        try:
            await callback.bot.delete_message(
                callback.from_user.id,
                (await get_msg_to_delete(callback.from_user.id))
            )
        except:
            pass

        await callback.message.delete()

        await set_msg_to_delete(callback.from_user.id,
                                (await callback.message.answer(
                                    text="Отправь мне ссылку трека 🔗 на SoundCloud 👇"
                                )).message_id)

        await state.set_state("free_attempts:link")
