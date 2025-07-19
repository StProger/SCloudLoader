import logging
import os

from pyrogram import Client
from pyrogram.types import Message

from bot.service import SoundCloud
from bot.settings import settings
from bot.celery_app import celery_app
import telebot

BOT_TOKEN = settings.BOT_TOKEN
bot = telebot.TeleBot(BOT_TOKEN)

@celery_app.task
def download_track_and_send(user_id: int, track_url: str, clock_message_id):
    downloaded_track = SoundCloud.download_track(
        track_url=track_url,
        user_id=user_id,
    )
    try:
        bot.delete_message(chat_id=user_id, message_id=clock_message_id)
    except:
        ...
    if downloaded_track:

        file_path = f'bot/service/sound_cloud/tracks/{user_id}'
        track_name = os.listdir(file_path)[0]
        logging.info(f"Трек: {track_name}")
        with Client("my_account.session") as app:
            if "zip" in track_name:
                message: Message = app.send_document(chat_id=settings.CHANNEL_ID_MUSIC, document=file_path + "/" + track_name)
            else:
                message: Message = app.send_audio(chat_id=settings.CHANNEL_ID_MUSIC, audio=file_path + "/" + track_name)
            os.remove(file_path + "/" + track_name)
            try:
                bot.copy_message(chat_id=user_id, from_chat_id=settings.CHANNEL_ID_MUSIC, message_id=message.id)
            except Exception as e:
                print(f"Ошибка при копировании сообщения: {e}")

    else:
        bot.send_message(chat_id=user_id, text="Не удалось скачать трек. Возможно, неправильная ссылка.")

