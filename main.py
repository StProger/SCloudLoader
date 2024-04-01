from bot.database.config import db, TORTOISE_CONFIG

import asyncio


async def main():

    try:
        await db.init(TORTOISE_CONFIG)

    except Exception as ex:
        print(ex)


if __name__ == '__main__':

    asyncio.run(main())