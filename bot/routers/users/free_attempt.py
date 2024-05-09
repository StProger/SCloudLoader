from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import Router, F, types, exceptions

from bot.filters.free_attempt import FreeAttempts
from bot.database.models.sub import Sub
from bot.database.models.user import User
from bot.keyboards.inline.user import not_subbed_markup, main_menu_key
from bot.service.redis_serv.user import get_msg_to_delete, set_msg_to_delete
from bot.service import SoundCloud

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

        downloaded_msg = await message.answer(
            text="Скачивание трека...⏳"
        )

        # Тут логика скачивания музыки и отправка
        downloaded_track = await SoundCloud.download_track(
            track_url=message.text,
            user_id=message.from_user.id,
            state=state
        )

        if downloaded_track == "NOT SUPPORTED":
            try:
                await message.bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=downloaded_msg.message_id
                )
            except:
                pass
            await message.answer("Данный трек недоступен для скачивания.",
                                 reply_markup=main_menu_key())

        elif downloaded_track is None:

            try:
                await message.bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=downloaded_msg.message_id
                )
            except:
                pass
            await message.answer(
                text="Произошла ошибка. Попробуйте позже снова."
            )
        else:

            state_data = await state.get_data()

            # Получаем данные о треке
            artist = state_data['artist']
            track_name = state_data['track_name']
            title = artist + " - " + track_name

            try:
                await message.bot.delete_message(
                    chat_id=message.chat.id,
                    message_id=downloaded_msg.message_id,
                    request_timeout=1
                )
                await message.delete()
            except:
                pass

            path_file = f"./bot/service/sound_cloud/tracks/{message.from_user.id}.wav"

            # Добавляем бесплатную попытку
            user.free_attempts = tortoise.expressions.F("free_attempts") + 1
            await user.save()

            # Отправляем трек
            await message.bot.send_audio(
                chat_id=message.chat.id,
                audio=types.FSInputFile(path_file),
                title=title,
                request_timeout=60
            )

            os.remove(path_file)
    await state.clear()


@router.message(FreeAttempts(), ~(F.text == "/term"))
async def free_attempts(
        message: types.Message,
        state: FSMContext
):

    await set_msg_to_delete(message.from_user.id,
                            (await message.answer(
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
