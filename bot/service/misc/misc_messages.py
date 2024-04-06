from aiogram import Bot
from aiogram.types import Message, CallbackQuery

from bot.keyboards.inline.user import main_inline
from bot.keyboards.inline.user import download_track_inline
from bot.keyboards.inline.user import choose_crypto_inline
from bot.keyboards.inline.user import choose_card_inline
from bot.service.redis_serv.user import set_msg_to_delete
from bot.settings import settings


async def main_menu(message: Message):

    await message.answer(
        text="Главное меню",
        reply_markup=main_inline()
    )


async def callback_main_menu(callback: CallbackQuery):

    await callback.message.edit_text(
        text="Главное меню",
        reply_markup=main_inline()
    )


async def download_track(
        callback: CallbackQuery
):

    await set_msg_to_delete(
        callback.from_user.id,
        (await callback.message.edit_text(
        text="Отправь мне ссылку трека 🔗 на SoundCloud 👇",
        reply_markup=download_track_inline()
            )).message_id
    )


async def crypto_menu(callback: CallbackQuery):

    PRICES = settings.PRICES

    text = f"""1 месяц - <b>{PRICES['crypto'][1]['price']}₽</b>
3 месяца - <b>{PRICES['crypto'][3]['price']}₽</b> ({PRICES['crypto'][3]['month']} за месяц)
6 месяцев - <b>{PRICES['crypto'][6]['price']}₽</b> ({PRICES['crypto'][6]['month']} за месяц)"""

    await callback.message.edit_text(
        text=text,
        reply_markup=choose_crypto_inline()
    )


async def card_menu(callback: CallbackQuery):

    PRICES = settings.PRICES

    text = f"""1 месяц - <b>{PRICES['card'][1]['price']}₽</b>
3 месяца - <b>{PRICES['card'][3]['price']}₽</b> 
6 месяцев - <b>{PRICES['card'][6]['price']}₽</b>"""

    await callback.message.edit_text(
        text=text,
        reply_markup=choose_card_inline()
    )