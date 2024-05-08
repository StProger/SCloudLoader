from aiogram import Bot
from aiogram.types.bot_command import BotCommand


async def set_bot_commands(bot: Bot):
    user_commands = [
        BotCommand(command="start", description="Главное меню"),
        BotCommand(command="term", description="Пользовательское соглашение")
    ]

    await bot.set_my_commands(commands=user_commands)
