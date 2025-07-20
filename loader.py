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
    with Client(
        "my_account",
        in_memory=True,
                session_string="AgGHP48AaYM5J0GZadPvJ2c8JKFHjceNnHZqwi1NUD-G9WFwzPBjWX3cMdWT39T4sqTyBgdfexLoT6h8ly3zTL_DCuJioWkLfz-l3_79RlnaPOJGShHCoOm8uEAYgRDm8vp41gplbVy9ajgwi7-TsJS7jJGLIGA_SszPEABLCcBcuSylOO2MRcXQ1YBxj2NRvM2MhxRGbxydwKGD2DJcFgABQ2Dde6cJSyJVGFQnAYpYeHHA0GGmknUlrPCZLKyWdhtPmhwhpNSNKuisMDDFIOQVb6aWyHXdRiqjn99B04dCIUCEfYbpZ_hmFinoZQysDiWcWuGdW6uiwRtPD69hNm3LuXaFIQAAAAHZOFITAA") as app:
        app.send_message(-1002679124021, text="Greetings from **Pyrogram**!")


if __name__ == '__main__':
    main()
