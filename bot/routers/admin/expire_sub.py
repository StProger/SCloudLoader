from aiogram import Router, F, types
from aiogram.filters.command import Command, CommandObject

from bot.filters.admin_filter import IsAdmin

from bot.database.models.user import User


router = Router()


@router.message(IsAdmin(), Command("expire_sub"))
async def expire_sub_user(
        message: types.Message,
        command: CommandObject
):
    print(command.args)
    user: User = await User.get_or_none(username=command.args)

    await message.delete()

    if not user:

        await message.answer(
            text="Нет такого юзера❌"
        )
    else:

        if (await user.is_subscribed()):

            expire_sub = await user.expire_sub()

            await message.answer(
                text=f"Срок подписки: <code>{expire_sub}</code> дней."
            )
        else:

            await message.answer(
                text="У юзера нет подписки."
            )
