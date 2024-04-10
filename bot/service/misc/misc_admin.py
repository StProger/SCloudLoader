from aiogram import types

from bot.database.models.sub import Sub
from bot.keyboards.inline.admin import admin_menu_markup, admin_sub_markup, admin_sub_list_markup, \
    admin_del_sub



async def admin_menu(message: types.Message):
    """первое сообшение админ меню"""
    return await message.answer(
        text="""
<b>Админ меню</b>

<code>🔹Команды:</code>
""",
        reply_markup=admin_menu_markup()
    )



async def sub_main(message: types.Message):
    """обяз подписка главное меню"""

    return await message.answer(
        text="Админ-панель",
        reply_markup=admin_sub_markup()
    )


async def get_active_subs(message: types.Message):
    """вывод активных ОП"""
    subs_list = Sub.filter(is_active=True).all()

    if await subs_list.count() == 0:
        await message.answer("Нет активных ОП")
        return await sub_main(message)

    subs_list = [
        [s.id, s.title, s.is_bot] for s in await subs_list
    ]

    await message.answer(
        text="Выбрать:",
        reply_markup=admin_sub_list_markup(subs_list)
    )


async def sub_info(message: types.Message, sub_id: int):
    sub = await Sub.get(id=sub_id)

    await message.answer(
        text=f"""
Данные по ОП

Ресурс: {'🤖' if sub.is_bot else '🚪'}
{'Токен бота' if sub.is_bot else 'ID канала'}: <code>{sub.bot_token}</code>
Название кнопки: <code>{sub.title}</code>
Ссылка: <code>{sub.link}</code>

Переходов: <code>{sub.visits}</code>
""",
        reply_markup=admin_del_sub(sub_id)
    )



async def check_token_valid(bot_token: str, session) -> bool:
    from aiogram import Bot
    try:
        bot = Bot(token=bot_token, session=session)
        await bot.get_me()
        return True
    except:
        return False