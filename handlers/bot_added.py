from aiogram import Router, types
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
# from keyboards.main_keyboard import get_main_keyboard
from keyboards.main_keyboard import get_main_keyboard_group

from config import ALLOWED_GROUP_ID

router = Router()



@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> IS_MEMBER))
async def bot_added_to_group(event: types.ChatMemberUpdated):
    if event.chat.type not in ["group", "supergroup"]:
        return

    # Если группа не та — выходим
    if event.chat.id != ALLOWED_GROUP_ID:
        await event.bot.leave_chat(event.chat.id)
        await event.bot.send_message(event.from_user.id, f"Бот работает только в определённой группе. Он покинул эту.")
        return

    # Проверка создателя (необязательно, но можно оставить)
    from utils.check_owner import is_group_owner
    if not await is_group_owner(event.bot, event.chat.id, event.from_user.id):
        await event.bot.leave_chat(event.chat.id)
        await event.bot.send_message(event.from_user.id, "❌ Только создатель группы может добавить бота.")
        return

    await event.bot.send_message(
        event.chat.id,
        "✅ Бот готов. Используйте кнопки.",
        reply_markup=get_main_keyboard_group()
    )

        # Получаем username бота для ссылки
    bot_info = await event.bot.get_me()
    bot_username = bot_info.username

    # Создаём инлайн-кнопку с ссылкой на диалог с ботом
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    url = f"https://t.me/{bot_username}?start=group"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📩 Написать боту (начать диалог)", url=url)]
        ]
    )

    # Отправляем сообщение в группу с инструкцией и кнопкой
    await event.bot.send_message(
        event.chat.id,
        "✅ Бот добавлен. Чтобы получать ответы в личные сообщения, нажмите на кнопку ниже и отправьте /start в открывшемся чате.\n"
        "После этого все команды из группы будут приходить вам в личку.",
        reply_markup=keyboard
    )