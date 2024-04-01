from tortoise.models import Model
from tortoise import fields

from datetime import datetime

import pytz

from bot.settings import settings


class User(Model):
    """ Таблица с пользователями """

    user_id = fields.BigIntField(pk=True, unique=True)

    # @username пользователя
    username = fields.CharField(max_length=64, null=True)

    # Дата регистрации
    created_at = fields.DatetimeField(auto_now_add=True, null=True)

    # Данные пользователя
    first_name = fields.TextField(null=True)
    last_name = fields.TextField(null=True)
    full_name = fields.TextField(null=True)
    language_code = fields.CharField(max_length=5, null=True)

    # Дата окончания подписки
    subscription_to = fields.DatetimeField(null=True, default=datetime.now)

    class Meta:
        table = "users"

    async def is_subscribed(self) -> bool:
        """ Есть ли у человека подписка """

        return datetime.now(tz=pytz.timezone(settings.BOT_TIMEZONE)) < self.subscription_to

