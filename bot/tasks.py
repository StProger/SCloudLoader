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
    print(f'Downloaded: {downloaded_track}')
    try:
        bot.delete_message(chat_id=user_id, message_id=clock_message_id)
    except:
        ...
    if downloaded_track:
        print(f"Send track...")

        file_path = f'bot/service/sound_cloud/tracks/{user_id}'
        archive_track_path = f'bot/service/sound_cloud/tracks/archive'
        archive_file_path = os.path.join(archive_track_path, str(user_id))
        track_name = os.listdir(file_path)
        if not track_name:
            archive_track_name = os.listdir(archive_file_path)
            print(f"Треки в архиве: {archive_track_name}")
            if archive_track_name:
                track_name = archive_track_name[0]
        else:
            track_name = track_name[0]
        print(f"Трек: {track_name}")
        print('Connecting to client...')
        with Client("my_account", in_memory=True, session_string=settings.PYRO_SESSION_STRING) as app:
            print("Connected to client complete...")

            if "zip" in track_name:
                document = os.path.join(archive_file_path, track_name)
                message: Message = app.send_document(chat_id=settings.CHANNEL_ID_MUSIC, document=document)
                try:
                    os.remove(document)
                except Exception as ex:
                    logging.error(ex)
            else:
                audio = os.path.join(file_path, track_name)
                message: Message = app.send_audio(chat_id=settings.CHANNEL_ID_MUSIC, audio=audio)
                try:
                    os.remove(audio)
                except Exception as ex:
                    logging.error(ex)

            try:
                bot.copy_message(chat_id=user_id, from_chat_id=settings.CHANNEL_ID_MUSIC, message_id=message.id)
            except Exception as e:
                print(f"Ошибка при копировании сообщения: {e}")

    else:
        bot.send_message(chat_id=user_id, text="Не удалось скачать трек. Возможно, неправильная ссылка.")

