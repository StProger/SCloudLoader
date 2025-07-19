from pyrogram import Client

# from bot.settings import settings


# client = Client(
#         "my_account",
#     )

def main():
    # client = Client(
    #     "client",
    #     api_hash=settings.API_HASH,
    #     api_id=settings.API_ID
    # )
    # await client.send_message(chat_id=-2679124021, text="Greetings from **Pyrogram**!")
    with Client("../my_account") as app:
        app.send_message(-1002679124021, text="Greetings from **Pyrogram**!")


if __name__ == '__main__':
    main()
