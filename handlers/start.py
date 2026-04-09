from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.main_keyboard import get_main_keyboard

router = Router()

@router.message(F.chat.type == "private", Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот, который помогает взаимодействовать с сайтом. Используй кнопки ниже:",
        reply_markup=get_main_keyboard()
    )