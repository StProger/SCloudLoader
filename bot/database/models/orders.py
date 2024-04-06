from tortoise.models import Model

from tortoise import fields


class Order(Model):
    """ Таблица с обязательными подписками """

    order_id = fields.IntField(pk=True, unique=True)

    # Кол-во месяцев
    count_month = fields.IntField(null=False)

    user_id = fields.BigIntField(null=False)

    class Meta:

        table = "orders"
