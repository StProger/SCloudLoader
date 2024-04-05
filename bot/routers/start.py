from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext

from bot.filters.free_attempt import FreeAttempts
from bot.service.misc.misc_messages import main_menu, callback_main_menu


router = Router()


@router.message(CommandStart(), StateFilter("*"), ~FreeAttempts())
async def start_handler(
        message: types.Message,
        state: FSMContext
):

    await state.clear()
    await main_menu(message=message)

@router.callback_query(
    F.data == "menu"
)
async def menu_callback(
        callback: types.CallbackQuery,
        state: FSMContext
):

    await state.clear()

    await callback_main_menu(callback=callback)
