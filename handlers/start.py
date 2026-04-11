from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.main_keyboard import get_main_keyboard
from config import ALLOWED_GROUP_ID, CREATOR_ID

router = Router()


async def is_user_in_allowed_group(bot, user_id: int) -> bool:
    """
    Returns True if the user is a current member of the allowed group.
    The creator always passes regardless of membership status.
    """
    if user_id == CREATOR_ID:
        return True
    if ALLOWED_GROUP_ID == 0:
        return False
    try:
        member = await bot.get_chat_member(ALLOWED_GROUP_ID, user_id)
        return member.status not in ["left", "kicked"]
    except Exception:
        return False


@router.message(F.chat.type == "private", Command("start"))
async def cmd_start(message: Message):
    if not await is_user_in_allowed_group(message.bot, message.from_user.id):
        await message.answer(
            "❌ Этот бот доступен только участникам определённой группы.\n"
            "Вступите в группу и попробуйте снова."
        )
        return

    await message.answer(
        "Привет! Я бот, который помогает взаимодействовать с сайтом. "
        "Используй кнопки ниже:",
        reply_markup=get_main_keyboard()
    )