from pyrogram import Client
import asyncio

# from bot.settings import settings


# client = Client(
#         "my_account",
#     )

async def main():
    # client = Client(
    #     "client",
    #     api_hash=settings.API_HASH,
    #     api_id=settings.API_ID
    # )
    # await client.send_message(chat_id=-2679124021, text="Greetings from **Pyrogram**!")
    async with Client("my_account") as app:
        await app.send_message(-1002679124021, text="Greetings from **Pyrogram**!")


if __name__ == '__main__':
    asyncio.run(main())
