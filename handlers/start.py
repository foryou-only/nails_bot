from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.start_keyboard import get_start_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Нажмите кнопку «Старт», чтобы продолжить:",
        reply_markup=get_start_keyboard()
    )