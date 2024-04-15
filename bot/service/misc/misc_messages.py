from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from bot.keyboards.inline.user import main_inline, main_inline_admin
from bot.keyboards.inline.user import download_track_inline
from bot.keyboards.inline.user import choose_crypto_inline
from bot.keyboards.inline.user import choose_card_inline

from bot.service.redis_serv.user import set_msg_to_delete
from bot.service.payments.crypto_cloud.expecting_paid import expecting_paid_crypto
from bot.service.payments.crypto_cloud.crypto_cloud import CryptoCloud
from bot.service.redis_serv.user import set_pay_msg_delete
from bot.service.payments.lava.lava import LavaPayment
from bot.service.payments.lava.expecting_pay import expecting_paid_lava

from bot.settings import settings

from bot.database.models.orders import Order
from bot.database.models.user import User

import asyncio


async def main_menu(message: Message):

    await message.answer(
        text="Главное меню",
        reply_markup=main_inline()
    )


async def main_menu_admin(message: Message):

    await message.answer(
        text="Главное меню",
        reply_markup=main_inline_admin()
    )



async def callback_main_menu(callback: CallbackQuery):

    await callback.message.edit_text(
        text="Главное меню",
        reply_markup=main_inline()
    )

async def callback_main_admin_menu(callback: CallbackQuery):

    await callback.message.edit_text(
        text="Главное меню",
        reply_markup=main_inline_admin()
    )


async def download_track(
        callback: CallbackQuery
):

    await set_msg_to_delete(
        callback.from_user.id,
        (await callback.message.edit_text(
        text="""
Отправь мне ссылку трека 🔗 на SoundCloud 👇
""",
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
    asyncio.create_task(
        expecting_paid_crypto(
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


async def create_invoice_card_pay(
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
    new_invoice = await LavaPayment.create_invoice(
        amount=float(PRICES["crypto"][count_month]['price']),
        order=order,
        bot_session=callback.bot.session
    )

    link_pay_inline = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Оплатить", url=new_invoice["link"]
                )
            ]
        ]
    )

    invoice_id = new_invoice["uuid"]

    # Создаём таску на ожидание оплаты
    asyncio.create_task(
        expecting_paid_lava(
            bot_session=callback.bot.session,
            user_id=callback.from_user.id,
            user=user,
            invoice_id=invoice_id,
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



async def referal_system(
        callback: CallbackQuery,
        user: User
):
    user_id = callback.from_user.id

    # Получаем username бота для реферальной ссылки
    bot_info = await callback.bot.get_me()
    username_bot = bot_info.username

    ref_link = f"https://t.me/{username_bot}?start={user_id}"

    count_referals = await user.get_count_ref()

    msg_text = f"""
Хочешь подписку, не тратя денег?

Всё что тебе нужно сделать это скинуть своим друзьям эту ссылку — <code>{ref_link}</code>

Если твой друг перейдёт по ссылке, то ты получишь 7 дней бесплатной подписки!

Приглашать друзей — самый лучший способ, которым ты можешь помочь нам, а также легко получить подписку!

Спасибо за твою поддержку 💛

Количество приглашенных рефералов: {count_referals}"""

    await callback.message.edit_text(
        text=msg_text,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Меню", callback_data="menu"
                    )
                ]
            ]
        )
    )


async def admin_panel_main(callback: CallbackQuery):

    await callback.message.edit_text(
        text="""
<b>Админ меню</b>

<code>🔹Команды:</code>
        """,
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Включить подписку✅",
                        callback_data="switch_on_sub"
                    ),
                    InlineKeyboardButton(
                        text="Выключить подписку❌",
                        callback_data="switch_off_sub"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔐 Обяз. Подписка",
                        callback_data="sub"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📨 Рассылка",
                        callback_data="admin_mailing"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Меню",
                        callback_data="menu"
                    )
                ]
            ]
        )
    )