from aiogram import Router, types
from aiogram.filters import ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.main_keyboard import get_main_keyboard_group
from config import ALLOWED_GROUP_ID, CREATOR_ID

router = Router()


@router.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> IS_MEMBER)
)
async def bot_added_to_group(event: types.ChatMemberUpdated):
    if event.chat.type not in ["group", "supergroup"]:
        return

    adder_id = event.from_user.id

    # Only the bot creator may add the bot to any group
    if adder_id != CREATOR_ID:
        await event.bot.leave_chat(event.chat.id)
        try:
            await event.bot.send_message(
                adder_id,
                "❌ Только создатель бота может добавить его в группу. Бот покинул чат."
            )
        except Exception:
            pass
        return

    # The bot must only stay in the one allowed group
    if event.chat.id != ALLOWED_GROUP_ID:
        await event.bot.leave_chat(event.chat.id)
        await event.bot.send_message(
            adder_id,
            "❌ Бот работает только в одной определённой группе. Он покинул этот чат."
        )
        return

    # All checks passed — greet the group
    await event.bot.send_message(
        event.chat.id,
        "✅ Бот готов к работе. Используйте кнопки ниже.",
        reply_markup=get_main_keyboard_group()
    )

    bot_info = await event.bot.get_me()
    url = f"https://t.me/{bot_info.username}?start=group"
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📩 Написать боту (начать диалог)", url=url)]
        ]
    )
    await event.bot.send_message(
        event.chat.id,
        "ℹ️ Чтобы получать ответы в личные сообщения, нажмите кнопку ниже "
        "и отправьте /start в открывшемся чате.\n"
        "После этого все команды из группы будут приходить вам в личку.",
        reply_markup=keyboard
    )