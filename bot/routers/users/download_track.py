import asyncio

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
from bot.tasks import download_track_and_send

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
):

    try:

        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=(await get_msg_to_delete(message.from_user.id)),
            request_timeout=1
        )
    except:
        pass

    await state.clear()

    downloaded_msg = await message.answer(
        text="Скачивание трека...⏳"
    )
    download_track_and_send.delay(
        message.from_user.id,
        message.text,
        downloaded_msg.message_id
    )

