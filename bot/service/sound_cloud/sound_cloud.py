import logging

import yt_dlp
from aiogram.fsm.context import FSMContext

from sclib.asyncio import SoundcloudAPI, Track
import shutil

from pydub import AudioSegment

import asyncio, os

from ffmpeg.asyncio import FFmpeg
from sclib.sync import UnsupportedFormatError

from multiprocessing import Process


class SoundCloud():

    api = SoundcloudAPI()


    @classmethod
    def proces_download_track(cls,
                              file_path: str,
                              url: str):
        ydl_opts = {
            'outtmpl': os.path.join(file_path, '%(title)s.%(ext)s'),  # Путь и имя файла
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',  # Конвертация в WAV
                'preferredquality': '192',
            }],
            'quiet': False,  # True если не хотите видеть вывод
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        # try:
        #     os.system(f"yt-dlp -f mp3 -o '%(fulltitle)s_{filename}' -P {file_path} {url}")
        # except Exception as ex:
        #     print(f"Ошибка {ex[:40]}")

    @classmethod
    def download_track(cls,
                       track_url: str,
                       user_id: int) -> bool | None | str:
        """ Скачивание трека """
        try:

            file_path = f'bot/service/sound_cloud/tracks/{user_id}'
            file_path_archive = f"bot/service/sound_cloud/tracks/archive/{user_id}/"
            if not os.path.exists(file_path_archive):
                os.mkdir(file_path_archive)
            cls.proces_download_track(file_path=file_path, url=track_url)
            list_files = os.listdir(file_path)
            print(list_files)
            if len(list_files) > 1:

                shutil.make_archive(file_path_archive, "zip", file_path)
                list_files_archive = os.listdir(file_path_archive)
                print(list_files_archive)
                for file in list_files:
                    if "zip" not in file:
                        os.remove(file_path + "/" + file)

            print('Выход')
            return True
        except Exception as ex:
            logging.error(ex)
            return False

    @classmethod
    async def convert_mp3_to_wav(cls,
                                 user_id: int,
                                 filename: str):
        """ Конверт в wav """

        ffmpeg = (FFmpeg()
                  .option("y")
                  .input(f"bot/service/sound_cloud/tracks/{filename}")
                  .output(
            f"bot/service/sound_cloud/tracks/{filename.replace('.mp3', '')}.wav",
            {"codec:a": "pcm_s16le"},
            vn=None,
            f="wav",
        ))
        await ffmpeg.execute()
        print('Сконвертил')

        # sound = AudioSegment.from_mp3(f"bot/service/sound_cloud/tracks/{user_id}.mp3")
        # sound.export(f"bot/service/sound_cloud/tracks/{user_id}.wav", format="wav")


async def main():

    await SoundCloud.download_track(
        track_url="https://on.api-core.soundcloud-stage.com/ZXUm9shL8MX2ZXhKNh",
        user_id=1878562358
    )

if __name__ == '__main__':
    asyncio.run(main())