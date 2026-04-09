from aiogram import Router, types
from aiogram.filters import Command
from filters.group_chat import GroupChatFilter
from keyboards.webapp_keyboard import get_site_webapp_keyboard
from keyboards.main_keyboard import get_main_keyboard_group
from config import ALLOWED_GROUP_ID

router = Router()
router.message.filter(GroupChatFilter())

async def allowed_group_filter(message: types.Message) -> bool:
    return message.chat.id == ALLOWED_GROUP_ID
router.message.filter(allowed_group_filter)

# Обработчик команды /start в группе – показываем клавиатуру в группе
@router.message(Command("start"))
async def start_in_group(message: types.Message):
    await message.answer(
        "Выберите действие:",
        reply_markup=get_main_keyboard_group()
    )
    await message.bot.send_message(
        message.from_user.id,
        "Привет! Я бот. Используйте кнопки в группе, ответы приходят в личку."
    )

@router.message(Command("help"))
async def help_in_group(message: types.Message):
    await message.bot.send_message(
        message.from_user.id,
        "Доступные команды:\n/start – показать кнопки в группе\n/help – помощь"
    )

# Обработчик кнопки "Написать боту" (отправляет ссылку в группу)
@router.message(lambda msg: msg.text == "📩 Написать боту")
async def group_contact_bot(message: types.Message):
    bot_info = await message.bot.get_me()
    await message.reply(
        f"📩 Напишите боту в личку: https://t.me/{bot_info.username}"
    )

# Универсальный обработчик для остальных reply-кнопок
@router.message()
async def handle_all_messages(message: types.Message):
    text = message.text
    user_id = message.from_user.id

    # По умолчанию parse_mode = None
    parse_mode = None

    if text == "🌐 Открыть сайт":
        reply_text = "Нажмите кнопку ниже, чтобы открыть сайт:"
        reply_markup = get_site_webapp_keyboard()
    elif text == "❓ Помощь":
        reply_text = "Доступные команды:\n/start – начать работу\n/help – помощь"
        reply_markup = None
    elif text == "ℹ️ О нас":
        reply_text = (
            "✨ О Нашем Проекте\n\n"
            "Привет! Я 🤖 Помощник, созданный, чтобы сделать ваше взаимодействие с нашим сервисом максимально удобным и быстрым.\n\n"
            "🚀 Мои возможности:\n"
            "• Мгновенный доступ к сайту — нажми на кнопку и откроется наш портал.\n"
            "• Оперативная поддержка — ответы на частые вопросы.\n"
            "• Новости и обновления — будьте в курсе всех событий.\n\n"
            "👨‍💻 О разработчике:\n"
            "Создан с ❤️ командой Urek-Mazino.\n"
            "«Мы делаем технологии ближе и понятнее»\n\n"
            "📆 Версия: 1.0.0"
        )
        reply_markup = None
    else:
        # Неизвестное сообщение – игнорируем
        return

    try:
        await message.bot.send_message(
            user_id,
            reply_text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
    except Exception as e:
        print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")