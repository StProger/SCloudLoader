from pyrogram import Client
import asyncio

from bot.settings import settings


client = Client(
        "client",
    )

async def main():
    client = Client(
        "client",
        api_hash=settings.API_HASH,
        api_id=settings.API_ID
    )
    await client.send_message(chat_id="me", text="Greetings from **Pyrogram**!")
    # async with Client("client", api_hash=settings.API_HASH,
    #     api_id=settings.API_ID) as app:
    #     await app.send_message(chat_id="me", text="Greetings from **Pyrogram**!")


if __name__ == '__main__':
    asyncio.run(main())
