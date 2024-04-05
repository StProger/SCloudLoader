from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.session.base import BaseSession

from bot.settings import settings


class CryptoCloud(object):

    headers = {
        "Authorization": f"Token {settings.CRYPTO_CLOUD_API_TOKEN}",
        "Content-Type": "application/json"
    }

    @classmethod
    async def create_invoice(cls,
                             amount: int | str,
                             order_id: int,
                             bot_session: AiohttpSession) -> dict | None:

        url = f"{settings.CRYPTO_CLOUD_API_URL}/invoice/create"
        session = await bot_session.create_session()

        body = {
            "amount": amount,
            "currency": "RUB",
            "shop_id": settings.SHOP_ID,
            "order_id": order_id
        }

        response = await session.post(url, headers=cls.headers, json=body)

        if response.status == 200:

            data = (await response.json())["result"]
            return {"link": data["link"], "uuid": data["uuid"]}

        else:
            return

    @classmethod
    async def merchant_info(cls,
                            uuid_merchant,
                            bot_session: AiohttpSession) -> dict | None:

        url = f"{settings.CRYPTO_CLOUD_API_URL}/invoice/merchant/info"

        body = {
            "uuids": [uuid_merchant]
        }

        session = await bot_session.create_session()

        response = await session.post(url, headers=cls.headers, json=body)

        if response.status == 200:

            data = (await response.json())["result"]

            return {"status_merchant": data["status"], "order_id": int(data["order_id"])}

        else:

            return
