from asyncio import sleep

from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.session.base import BaseSession

from bot.database.models.user import User
from bot.database.models.orders import Order

from bot.service.payments.lava.lava import LavaPayment
from bot.service.redis_serv.user import get_pay_msg_delete

from aiogram import Bot, types

from datetime import timedelta


async def expecting_paid_lava(
        bot: Bot,
        user_id: int,
        user: User,
        invoice_id: str,
        bot_session: AiohttpSession | BaseSession,
        order: Order
) -> None:
    """ Проверка оплаты картой """

    menu_inline = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Меню", callback_data="menu"
                ),
                types.InlineKeyboardButton(
                    text="Подписка💸", callback_data="sub_user"
                )
            ]
        ]
    )

    while True:

        merchant_info = await LavaPayment.merchant_info(
            invoice_id=invoice_id,
            order_id=order.order_id,
            bot_session=bot_session
        )

        if merchant_info["status"] != "success":

            if (await order.left_time()) >= 10:

                try:
                    await bot.delete_message(
                        chat_id=user_id,
                        message_id=(await get_pay_msg_delete(user_id)),
                        request_timeout=1
                    )
                except:
                    pass

                await bot.send_message(
                    chat_id=user_id,
                    text="Время на оплату подписки истекло❌",
                    reply_markup=menu_inline
                )
                return
            else:
                await sleep(7)

        else:

            order.status_paid = True
            count_month = order.count_month
            user.subscription_to = (user.subscription_to + timedelta(days=count_month * 30))
            await user.save()
            await order.save()
            try:
                await bot.delete_message(
                    chat_id=user_id,
                    message_id=(await get_pay_msg_delete(user_id)),
                    request_timeout=1
                )
            except:
                pass
            await bot.send_message(
                chat_id=user_id,
                text="Оплата подписки прошла успешно✅",
                reply_markup=menu_inline
            )
            return
