from aiogram import Router, types
from aiogram.filters import Command
from filters.group_chat import GroupChatFilter
from keyboards.webapp_keyboard import get_site_webapp_keyboard
from keyboards.main_keyboard import get_main_keyboard_group 
from config import ALLOWED_GROUP_ID
from config import GROUP_USERNAME

router = Router()
router.message.filter(GroupChatFilter())  # только групповые чаты



# Фильтр для проверки ID разрешённой группы (опционально)
async def allowed_group_filter(message: types.Message) -> bool:
    return message.chat.id == ALLOWED_GROUP_ID

router.message.filter(allowed_group_filter)

# Обработчик команды /start в группе
@router.message(Command("start"))
async def start_in_group(message: types.Message):
    await message.bot.send_message(
        message.from_user.id,
        "Привет! Я бот. Используйте кнопки ниже для взаимодействия:",
        reply_markup=get_main_keyboard_group()
    )

# Обработчик команды /help в группе
@router.message(Command("help"))
async def help_in_group(message: types.Message):
    await message.bot.send_message(
        message.from_user.id,
        "Доступные команды:\n/start – начать работу\n/help – помощь\n\n"
        "Используйте кнопки в группе, чтобы получить нужную клавиатуру в личку."
    )

@router.message(lambda msg: msg.text == "📩 Написать боту")
async def group_contact_bot(message: types.Message):
    bot_info = await message.bot.get_me()
    await message.answer(  # или message.reply, но answer отправляет в тот же чат
        f"Напишите боту в личку: https://t.me/{bot_info.username}"
    )

# @router.message(lambda msg: msg.text == "📩 Написать боту")
# async def group_contact_bot(message: types.Message):
#     bot_info = await message.bot.get_me()
#     await message.answer(  # или message.reply, но answer отправляет в тот же чат
#         f"👥 Вот ссылка на нашу группу: https://t.me/{GROUP_USERNAME}"
#     )




# Универсальный обработчик всех текстовых сообщений в группе (включая нажатия на reply-кнопки)
@router.message()
async def handle_all_messages(message: types.Message):
    text = message.text
    user_id = message.from_user.id

    # Определяем, какой ответ отправить в личку
    if text == "🌐 Открыть сайт":
        reply_text = "Нажмите кнопку ниже, чтобы открыть сайт:"
        reply_markup = get_site_webapp_keyboard()
    elif text == "❓ Помощь":
        reply_text = "Доступные команды:\n/start – начать работу"
        reply_markup = None
    elif text == "ℹ️ О нас":
        reply_text = (
        "<b>✨ О Нашем Проекте</b>\n\n"
        "Привет! Я <b>🤖 Помощник</b>, созданный, чтобы сделать ваше взаимодействие с нашим сервисом максимально удобным и быстрым.\n\n"
        "<b>🚀 Мои возможности:</b>\n"
        "• <b>Мгновенный доступ к сайту</b> — нажми на кнопку и откроется наш портал.\n"
        "• <b>Оперативная поддержка</b> — ответы на частые вопросы.\n"
        "• <b>Новости и обновления</b> — будьте в курсе всех событий.\n\n"
        "<b>👨‍💻 О разработчике:</b>\n"
        "Создан с ❤️ командой Urek-Mazino.\n"
        "<i>«Мы делаем технологии ближе и понятнее»</i>\n\n"
        "📆 Версия: <code>1.0.0</code>"
    )
        reply_markup = None
        
        await message.bot.send_message(
            user_id,
            reply_text,
            reply_markup=reply_markup,
            parse_mode="HTML"   # <-- добавьте эту строку
    )
    else:
        # Если сообщение не соответствует ни одной кнопке – игнорируем
        return

    try:
        await message.bot.send_message(
            user_id,
            reply_text,
            reply_markup=reply_markup
        )
        # Если бот администратор, можно удалить исходное сообщение из группы
        # try:
        #     await message.delete()
        # except:
        #     pass
    except Exception as e:
        print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")