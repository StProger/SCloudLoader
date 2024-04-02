from tortoise.models import Model

from tortoise import fields


class Sub(Model):
    """ Таблица с обязательными подписками """

    id = fields.IntField(pk=True, unique=True)

    is_bot = fields.BooleanField(default=False)  # бот или нет
    is_active = fields.BooleanField(default=True)

    title = fields.TextField()  # название оп
    link = fields.TextField()  # ссылка на клиента
    bot_token = fields.TextField()  # токен если это бот

    visits = fields.BigIntField(default=0)

    created_at = fields.DatetimeField(auto_now_add=True, null=False)

    class Meta:
        table = "subs"
