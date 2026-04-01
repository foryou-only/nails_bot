from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Доступные команды:\n"
        "/start - начать работу\n"
        "/help - справка\n\n"
        "Также вы можете использовать кнопки внизу экрана."
    )