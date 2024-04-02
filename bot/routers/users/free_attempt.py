from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, types, exceptions

from bot.filters.free_attempt import FreeAttempts
from bot.database.models.sub import Sub
from bot.database.models.user import User
from bot.keyboards.inline.user import not_subbed_markup


router = Router()

NOT_SUBBED = """
Подпишитесь на наши каналы!
"""


@router.message(FreeAttempts())
async def free_attempts(
        message: types.Message,
        state: FSMContext
):

    await message.answer(
        text="Отправь мне ссылку трека 🔗 на SoundCloud 👇"
    )

    await state.set_state("free_attempts:link")


@router.message(StateFilter("free_attempts:link"))
async def download_music(
        message: types.Message,
        sponsors: list[Sub],
        state: FSMContext,
        user: User
):

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

        await callback.message.delete()
        await callback.message.answer(
            text="Отправь мне ссылку трека 🔗 на SoundCloud 👇"
        )

        await state.set_state("free_attempts:link")
