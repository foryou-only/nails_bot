from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.main_keyboard import get_main_keyboard

router = Router()
# @router.message(Command("getid"))
# async def get_chat_id(message: type.Message):
#     await message.answer(f"ID этого чата: {message.chat.id}")
# @router.message(Command("start"))
# async def cmd_start(message: Message):
#     """Обработчик команды /start, показывает основные кнопки."""
#     await message.answer(
#         "Привет! Я бот, который помогает взаимодействовать с сайтом. Используй кнопки ниже:",
#         reply_markup=get_main_keyboard()
#     )

from keyboards.main_keyboard import get_main_keyboard

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я бот, который помогает взаимодействовать с сайтом. Используй кнопки ниже:", reply_markup=get_main_keyboard())