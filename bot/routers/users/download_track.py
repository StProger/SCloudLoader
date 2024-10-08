from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from pyrogram import Client

from bot.database.models.user import User
from bot.service.misc.misc_messages import download_track
from bot.service.redis_serv.user import get_msg_to_delete
from bot.service.sound_cloud.sound_cloud import SoundCloud
from bot.keyboards.inline.user import main_menu_key

import os

from bot.settings import settings

router = Router()


@router.callback_query(
    F.data == "download_track"
)
async def get_link_track(
        callback: types.CallbackQuery,
        state: FSMContext,
        user: User
):
    """ Кнопка "Скачать трек" """

    if not (await user.is_subscribed()):

        await callback.answer("У вас нет подписки❌",
                              show_alert=True)
    else:

        await state.set_state("download_track:link")
        await download_track(callback=callback)


@router.message(
    StateFilter("download_track:link"), F.text
)
async def download_track_(
        message: types.Message,
        state: FSMContext,
        client: Client
):

    try:

        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=(await get_msg_to_delete(message.from_user.id)),
            request_timeout=1
        )
    except:
        pass

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
        await message.answer("Произошла ошибка. Убедитесь в корректности ссылки.",
                             reply_markup=main_menu_key())
    else:

        state_data = await state.get_data()

        # Получаем данные о треке
        title_track = state_data["title_track"]
        filename_track = state_data["filename"]
        filename_track = filename_track.replace("'", "")

        try:
            await message.bot.delete_message(
                chat_id=message.chat.id,
                message_id=downloaded_msg.message_id,
                request_timeout=1
            )
            await message.delete()
        except:
            pass

        path_file = f"bot/service/sound_cloud/tracks/{filename_track}"
        print(path_file)
        # Отправляем трек

        mes = await client.send_audio(
            chat_id=settings.CHANNEL_ID_MUSIC,
            audio=path_file,
            title=title_track
        )

        await message.bot.copy_message(
            chat_id=message.from_user.id,
            from_chat_id=settings.CHANNEL_ID_MUSIC,
            message_id=mes.id
        )

        # await message.bot.send_audio(
        #     chat_id=message.chat.id,
        #     audio=types.FSInputFile(path_file),
        #     title=title_track,
        #     request_timeout=180
        # )

        os.remove(path_file)

    await state.clear()
