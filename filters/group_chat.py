from aiogram.filters import BaseFilter
from aiogram.types import Message

class GroupChatFilter(BaseFilter):
    """Фильтр для обработки сообщений только из групп и супергрупп."""
    async def __call__(self, message: Message) -> bool:
        return message.chat.type in ["group", "supergroup"]