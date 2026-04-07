from aiogram import Bot

async def is_group_owner(bot: Bot, chat_id: int, user_id: int) -> bool:
    """
    Проверяет, является ли пользователь создателем группы.
    Этот метод не требует, чтобы бот был администратором.
    """
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        return member.status == "creator"
    except Exception:
        return False