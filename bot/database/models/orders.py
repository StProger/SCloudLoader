import pytz

from tortoise.models import Model
from tortoise import fields

from datetime import datetime

from bot.settings import settings


class Order(Model):
    """ Таблица с обязательными подписками """

    order_id = fields.IntField(pk=True, unique=True)

    # Кол-во месяцев
    count_month = fields.IntField(null=False)

    user_id = fields.BigIntField(null=False)

    created_at = fields.DatetimeField(null=False, default=datetime.now(tz=pytz.timezone(settings.BOT_TIMEZONE)))

    status_paid = fields.BooleanField(default=False)

    class Meta:

        table = "orders"

    async def left_time(self):
        """ Получить кол-во минут после создания заказа """

        return (datetime.now(tz=pytz.timezone(settings.BOT_TIMEZONE)) - self.created_at).total_seconds() / 60.0
