from pydantic_settings import BaseSettings

from dotenv import load_dotenv

import os, json

from yarl import URL


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

    ADMIN_IDS: list[int] = []

    # Домен API CryptoCloud
    CRYPTO_CLOUD_API_URL: str = "https://api.cryptocloud.plus/v2"

    # shop_id CryptoCloud
    SHOP_ID: str = os.getenv("SHOP_ID").strip()

    # Токен CryptoCloud
    CRYPTO_CLOUD_API_TOKEN = os.getenv("CRYPTO_CLOUD_API_TOKEN").strip()


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
