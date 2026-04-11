from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from config import ALLOWED_GROUP_ID

router = Router()


async def is_user_in_allowed_group(bot, user_id: int) -> bool:
    if ALLOWED_GROUP_ID == 0:
        return False
    try:
        member = await bot.get_chat_member(ALLOWED_GROUP_ID, user_id)
        return member.status not in ["left", "kicked"]
    except Exception:
        return False


@router.message(F.chat.type == "private", Command("help"))
async def help_command(message: Message):
    if not await is_user_in_allowed_group(message.bot, message.from_user.id):
        await message.answer("❌ Доступ только для участников группы.")
        return

    await message.answer(
        "Доступные команды:\n"
        "/start — начать работу\n"
        "/help — справка\n\n"
        "Также вы можете использовать кнопки внизу экрана."
    )