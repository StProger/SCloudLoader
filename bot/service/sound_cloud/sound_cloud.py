from aiogram.fsm.context import FSMContext

from sclib.asyncio import SoundcloudAPI, Track

from pydub import AudioSegment

import asyncio, os

from ffmpeg.asyncio import FFmpeg
from sclib.sync import UnsupportedFormatError

from multiprocessing import Process


class SoundCloud(object):

    api = SoundcloudAPI()


    @classmethod
    def proces_download_track(cls,
                              filename: str,
                              file_path: str,
                              url: str):

        os.system(f"yt-dlp -f mp3 %(fulltitle)s_{filename} -P {file_path} {url}")

    @classmethod
    async def download_track(cls,
                             track_url: str,
                             user_id: int,
                             state: FSMContext | None = None,) -> bool | None | str:
        """ Скачивание трека """
        # try:
        if 1 == 1:
            filename = f'{user_id}.mp3'
            file_path = f'bot/service/sound_cloud/tracks'

            process_download = Process(target=cls.proces_download_track, args=(filename, file_path, track_url))

            process_download.start()
            process_download.join()
            print("начал качать")
            list_files = os.listdir(file_path)

            file_name_track = (list(filter(lambda file_: f"{user_id}.mp3" in file_, list_files)))[0]
            print(file_name_track)

            title = file_name_track.split('_', maxsplit=1)[0]

            # try:
            #     track: Track = await cls.api.resolve(track_url.replace("m.", "", 1))
            # except KeyError:
            #     return
            #
            # if track is None:
            #     return

            await state.update_data(
                title_track=title,
                filename=file_name_track.replace(".mp3", ".wav")
            )

            # with open(filename, 'wb+') as file:
            #     await track.write_mp3_to(file)

            await cls.convert_mp3_to_wav(
                user_id=user_id,
                filename=file_name_track
            )
            for file in list_files:
                os.remove(file_path + "/" + file)

            return True
        # except Exception as ex:
        #     print(ex)
        #     return

    @classmethod
    async def convert_mp3_to_wav(cls,
                                 user_id: int,
                                 filename: str):
        """ Конверт в wav """

        ffmpeg = (FFmpeg()
                  .option("y")
                  .input(f"bot/service/sound_cloud/tracks/{filename}")
                  .output(
            f"bot/service/sound_cloud/tracks/{filename.replace(".mp3", "")}.wav",
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
        track_url="https://soundcloud.com/itsmeneedle/sunday-morning",
        user_id=1878562358
    )

if __name__ == '__main__':
    asyncio.run(main())