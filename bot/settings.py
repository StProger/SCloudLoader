from pydantic_settings import BaseSettings

from dotenv import load_dotenv

import os, json

from yarl import URL

from apscheduler.schedulers.asyncio import AsyncIOScheduler


load_dotenv()


class Settings(BaseSettings):

    BOT_TIMEZONE: str = os.getenv("BOT_TIMEZONE").strip() or "Europe/Moscow"
    BOT_TOKEN: str = os.getenv("BOT_TOKEN").strip()

    DB_PASSWORD: str = os.getenv("DB_PASSWORD").strip()
    DB_NAME: str = os.getenv("DB_NAME").strip()
    DB_HOST: str = os.getenv("DB_HOST").strip()
    DB_PORT: int = int(os.getenv("DB_PORT").strip())
    DB_USER: str = os.getenv("DB_USER").strip()

    FSM_REDIS_HOST: str = os.getenv("FSM_REDIS_HOST").strip()
    FSM_REDIS_DB: int = os.getenv("FSM_REDIS_DB").strip()

    REDIS_HOST: str = os.getenv("REDIS_HOST").strip()
    REDIS_DB: int = os.getenv("REDIS_DB").strip()

    # Путь к логам
    PATH_LOGS: str = "bot/data/logs.log"

    ADMIN_IDS: list[int] = json.loads(os.getenv("ADMIN_IDS"))

    # Домен API CryptoCloud
    CRYPTO_CLOUD_API_URL: str = "https://api.cryptocloud.plus/v2"

    # shop_id CryptoCloud
    SHOP_ID_CRYPTO_CLOUD: str = os.getenv("SHOP_ID_CRYPTO_CLOUD").strip()

    # shop_id LAVA
    SHOP_ID_LAVA: str = os.getenv("SHOP_ID_LAVA").strip()

    # secretKey LAVA
    SECRET_KEY_LAVA: str = os.getenv("SECRET_KEY_LAVA").strip()

    # Домен API LAVA
    LAVA_API_URL: str = os.getenv("LAVA_API_URL").strip()

    # Токен CryptoCloud
    CRYPTO_CLOUD_API_TOKEN: str = os.getenv("CRYPTO_CLOUD_API_TOKEN").strip()

    # Публичная оферта
    public_offer: str = "https://docs.google.com/document/d/1uQXkIOMF_OJDTjCtaRZiRfVs_ZEDEu2-3ksDEt9lRXI"
    # Обработка персональных данных
    personal_data: str = "https://docs.google.com/document/d/1meffmKDtaO9G5wZ_G6-O7xt8V7WnukFMkRWHtTsmJlI"

    # Цены подписки
    PRICES: dict = {
        "crypto": {
            1: {
                "price": 50,
                "month": None
            },
            3: {
                "price": 2399,
                "month": 799
            },
            6: {
                "price": 4199,
                "month": 699
            }
        },
        "card": {
            1: {
                "price": 1099,
                "month": None
            },
            3: {
                "price": 2499,
                "month": None
            },
            6: {
                "price": 4299,
                "month": None
            }
        }
    }

    @property
    def db_url(self):
        """
        Создание ссылки для подключения к базе данных

        :return:
        """

        return URL.build(
            scheme="asyncpg",
            host=self.DB_HOST,
            port=self.DB_PORT,
            user=self.DB_USER,
            password=self.DB_PASSWORD,
            path=f"/{self.DB_NAME}",
        )

    @property
    def fsm_redis_url(self) -> str:
        """
        создание URL для подключения к редису

        :return: redis connection url
        """
        return str(URL.build(
            scheme="redis",
            host=self.FSM_REDIS_HOST,
            path="/" + str(self.FSM_REDIS_DB)
        ))


settings = Settings()
BOT_SCHEDULER = AsyncIOScheduler(timezone=settings.BOT_TIMEZONE)
