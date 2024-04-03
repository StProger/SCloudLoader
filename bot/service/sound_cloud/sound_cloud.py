from aiogram.fsm.context import FSMContext

from sclib.asyncio import SoundcloudAPI, Track

import aiofiles

# from pydub import AudioSegment

import asyncio


class SoundCloud(object):

    api = SoundcloudAPI()

    @classmethod
    async def download_track(cls,
                             track_url: str,
                             user_id: int,
                             state: FSMContext | None = None,) -> bool | None:
        """ Скачивание трека """

        track: Track = await cls.api.resolve(track_url)

        if track is None:
            return

        # assert type(track) is Track

        filename = f'tracks/{user_id}.mp3'

        # await state.update_data(
        #     artist=track.artist,
        #     track_name=track.title
        # )

        async with aiofiles.open(filename, 'wb+') as file:
            await track.write_mp3_to(file)

        #

        return True

    # @classmethod
    # async def convert_mp3_to_wav(cls,
    #                              user_id: int):
    #     """ Конверт в wav """
    #
    #     sound = AudioSegment.from_mp3(f"{user_id}.mp3")
    #     sound.export(f"{user_id}.wav", format="wav")


async def main():

    await SoundCloud.download_track(
        track_url="https://soundcloud.com/itsmeneedle/sunday-morning",
        user_id=1878562358
    )

if __name__ == '__main__':
    asyncio.run(main())