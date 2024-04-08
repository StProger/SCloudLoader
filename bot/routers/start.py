from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.filters.command import CommandStart
from aiogram.fsm.context import FSMContext

from bot.filters.free_attempt import FreeAttempts
from bot.service.misc.misc_messages import (main_menu,
                                            callback_main_menu,
                                            main_menu_admin,
                                            callback_main_admin_menu)
from bot.filters.admin_filter import IsAdmin


router = Router()


@router.message(
    IsAdmin(),
    CommandStart(),
    StateFilter("*")
)
async def start_admin_handler(
        message: types.Message,
        state: FSMContext
):

    await state.clear()
    await main_menu_admin(message)


@router.message(CommandStart(), StateFilter("*"), ~FreeAttempts())
async def start_handler(
        message: types.Message,
        state: FSMContext
):

    await state.clear()
    await main_menu(message=message)


@router.callback_query(
    IsAdmin(),
    F.data == "menu"
)
async def menu_callback_admin(
        callback: types.CallbackQuery,
        state: FSMContext
):

    await state.clear()

    await callback_main_admin_menu(callback=callback)


@router.callback_query(
    F.data == "menu"
)
async def menu_callback(
        callback: types.CallbackQuery,
        state: FSMContext
):

    await state.clear()

    await callback_main_menu(callback=callback)
