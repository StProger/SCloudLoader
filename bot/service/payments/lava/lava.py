import hashlib
import hmac

from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.session.base import BaseSession

from bot.database.models.orders import Order

from bot.settings import settings

import json


class LavaPayment(object):

    @staticmethod
    async def create_invoice(
            order: Order,
            amount: float,
            bot_session: AiohttpSession | BaseSession
    ) -> None | dict:

        request_body = {
            "expire": 10,
            "orderId": order.order_id,
            "shopId": settings.SHOP_ID_LAVA,
            "sum": amount
        }

        json_str = json.dumps(request_body).encode()

        sign = hmac.new(bytes(settings.SECRET_KEY_LAVA, 'UTF-8'), json_str, hashlib.sha256).hexdigest()

        headers = {
            'Content-Type': 'application/json',
            "Accept": "application/json",
            "Signature": sign
        }

        session = await bot_session.create_session()

        url = f"{settings.LAVA_API_URL}/invoice/create"

        response = await session.post(
            url=url,
            headers=headers,
            data=json.dumps(request_body)
        )

        if response.status == 200:

            data = (await response.json())["data"]
            return {"link": data["url"], "uuid": data["id"]}
        else:

            return

    @staticmethod
    async def merchant_info(
            invoice_id: str,
            bot_session: AiohttpSession | BaseSession,
            order_id: str
    ):

        request_body = {
            "shopId": settings.SHOP_ID_LAVA,
            "orderId": order_id,
            "invoiceId": invoice_id
        }

        json_str = json.dumps(request_body).encode()

        sign = hmac.new(bytes(settings.SECRET_KEY_LAVA, 'UTF-8'), json_str, hashlib.sha256).hexdigest()

        headers = {
            'Content-Type': 'application/json',
            "Accept": "application/json",
            "Signature": sign
        }

        url = f"{settings.LAVA_API_URL}/business/invoice/status"

        session = await bot_session.create_session()

        response = await session.post(
            url=url,
            headers=headers,
            data=json.dumps(request_body)
        )

        if response.status == 200:

            data = (await response.json())["data"]

            return {"status": data["status"]}

        else:

            return
