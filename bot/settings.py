from pydantic_settings import BaseSettings

from dotenv import load_dotenv

import os

from yarl import URL


load_dotenv()


class Settings(BaseSettings):

    BOT_TIMEZONE: str = os.getenv("BOT_TIMEZONE").strip() or "Europe/Moscow"
    DB_PASSWORD: str = os.getenv("DB_PASSWORD").strip()
    DB_NAME: str = os.getenv("DB_NAME").strip()
    DB_HOST: str = os.getenv("DB_HOST").strip()
    DB_PORT: int = int(os.getenv("DB_PORT").strip())
    DB_USER: str = os.getenv("DB_USER").strip()

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


settings = Settings()
