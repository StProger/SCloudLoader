from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, types, exceptions
from pyrogram import Client

from bot.filters.free_attempt import FreeAttempts
from bot.database.models.sub import Sub
from bot.database.models.user import User
from bot.keyboards.inline.user import not_subbed_markup, main_menu_key
from bot.service.redis_serv.user import get_msg_to_delete, set_msg_to_delete
from bot.service import SoundCloud
from bot.settings import settings
from bot.tasks import download_track_and_send

import os

import tortoise.expressions


router = Router()

NOT_SUBBED = """
Подпишитесь на наши каналы!
"""


@router.message(FreeAttempts(), F.text.contains("https"))
async def download_music(
        message: types.Message,
        sponsors: list[Sub],
        state: FSMContext,
        user: User,
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

        downloaded_msg = await message.answer(
            text="Скачивание трека...⏳"
        )

        # Тут логика скачивания музыки и отправка
        download_track_and_send.delay(
            message.from_user.id,
            message.text,
            downloaded_msg.message_id
        )
        user.free_attempts = user.free_attempts - 1
        await user.save()

    await state.clear()


@router.message(FreeAttempts(), ~(F.text == "/term"))
async def free_attempts(
        message: types.Message,
        state: FSMContext,
        user: User
):

    await set_msg_to_delete(message.from_user.id,
                            (await message.answer(
                                text=f"""
У вас есть <code>{2 - user.free_attempts}</code> <b>бесплатных попыток</b> скачать музыку.
Отправь мне ссылку трека 🔗 на SoundCloud 👇
""",
                                reply_markup=types.InlineKeyboardMarkup(
                                    inline_keyboard=[
                                        [
                                            types.InlineKeyboardButton(
                                                text="Как получить ссылку",
                                                url="https://telegra.ph/Poluchenie-ssylki-na-trek-SoundCloud-04-15"
                                            )
                                        ]
                                    ]
                                )
                            )).message_id,
                            )

    # await state.set_state("free_attempts:link")


@router.callback_query(F.data == "checksub")
async def subbed(callback: types.CallbackQuery,
                 user: User,
                 sponsors: list[Sub],
                 state: FSMContext):

    if bool(sponsors):

        await callback.answer("Вы не подписались❌")
    else:
        user.subbed = True

        if not user.subbed_before:
            user.subbed_before = True

            await Sub.filter(is_active=True).update(visits=tortoise.expressions.F("visits") + 1)

        await user.save()
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
                                    text="""
Отправь мне ссылку трека 🔗 на SoundCloud 👇
""",
                                    reply_markup=types.InlineKeyboardMarkup(
                                        inline_keyboard=[
                                            [
                                                types.InlineKeyboardButton(
                                                    text="Как получить ссылку",
                                                    url="https://telegra.ph/Poluchenie-ssylki-na-trek-SoundCloud-04-15"
                                                )
                                            ]
                                        ]
                                    )
                                )).message_id)

        await state.set_state("free_attempts:link")
