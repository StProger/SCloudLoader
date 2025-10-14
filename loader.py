from pyrogram import Client

# from bot.settings import settings


# client = Client(
#         "my_account",
#     )
API_HASH="f3564dd1d748e2b7724b8036d9b5f78b"
API_ID=13840126

def main():
    # client = Client(
    #     "client",
    #     api_hash=settings.API_HASH,
    #     api_id=settings.API_ID
    # )
    # await client.send_message(chat_id=-2679124021, text="Greetings from **Pyrogram**!")
    with Client(
        "client",
        api_hash=API_HASH, api_id=API_ID) as app:
        app: Client
        # app.send_message("kicode", "hi")
        app.send_message(-1002679124021, text="Greetings from **Pyrogram**!")


if __name__ == '__main__':
    main()
