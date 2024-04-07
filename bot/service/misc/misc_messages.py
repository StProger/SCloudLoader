from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.inline.user import main_inline
from bot.keyboards.inline.user import download_track_inline
from bot.keyboards.inline.user import choose_crypto_inline
from bot.keyboards.inline.user import choose_card_inline

from bot.service.redis_serv.user import set_msg_to_delete
from bot.service.payments.expecting_paid import expecting_paid
from bot.service.payments.crypto_cloud import CryptoCloud
from bot.service.redis_serv.user import set_pay_msg_delete

from bot.settings import settings

from bot.database.models.orders import Order
from bot.database.models.user import User

import asyncio


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


async def create_invoice_crypto_pay(
        callback: CallbackQuery,
        user: User
):

    PRICES = settings.PRICES
    count_month = int(callback.data.split("_")[-1])
    order: Order = await Order.create(
        count_month=count_month,
        user_id=callback.from_user.id
    )

    # Создаём новый инвойс на оплату
    new_invoice = await CryptoCloud.create_invoice(
        amount=PRICES["crypto"][count_month]['price'],
        order_id=order.order_id,
        bot_session=callback.bot.session
    )
    print(new_invoice)
    link_pay_inline = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Оплатить", url=new_invoice["link"]
                )
            ]
        ]
    )

    uuid_merchant = new_invoice["uuid"]

    # Создаём таску на ожидание оплаты
    await asyncio.create_task(
        expecting_paid(
            bot_session=callback.bot.session,
            user_id=callback.from_user.id,
            user=user,
            uuid=uuid_merchant,
            order=order,
            bot=callback.bot
        )
    )

    await set_pay_msg_delete(callback.from_user.id,
                             (await callback.message.edit_text(
                                text="Для оплаты нажмите кнопку ниже👇.\n"
                                     "У вас есть <b>10 минут</b> для оплаты.",
                                reply_markup=link_pay_inline
                                )).message_id)
