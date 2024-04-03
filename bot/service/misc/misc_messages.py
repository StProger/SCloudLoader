from aiogram import Bot
from aiogram.types import Message


async def input_link_free_attempt(message: Message):
    """ Пробный период """

    try:
        await message.delete()
    except:
        pass

    await message.answer(
        text="Отправь мне ссылку трека 🔗 на SoundCloud 👇"
    )
