from aiogram import Router, types, F
from aiogram.filters import Command
from filters.group_chat import GroupChatFilter
from keyboards.webapp_keyboard import get_site_webapp_keyboard
from keyboards.main_keyboard import get_main_keyboard_group
from config import ALLOWED_GROUP_ID, CREATOR_ID
import asyncio

router = Router()
router.message.filter(GroupChatFilter())
router.message.filter(F.chat.id == ALLOWED_GROUP_ID)


# ID закреплённого сообщения с клавиатурой для каждого чата
# Хранится в памяти: { chat_id: message_id }
_keyboard_message: dict[int, int] = {}

async def _delete(message: types.Message, delay: float = 0):
    """Удаляет сообщение. Если задержка — ждёт сначала. Молча игнорирует ошибки."""
    try:
        if delay:
            await asyncio.sleep(delay)
        await message.delete()
    except Exception:
        pass

async def _ensure_keyboard(message: types.Message):
    """
    Проверяет живо ли закреплённое сообщение с клавиатурой.
    Если нет — создаёт новое и сохраняет его ID.
    Само сообщение содержит пробел (невидимый текст) чтобы не мусорить чат,
    но клавиатура остаётся активной у всех участников.
    """
    chat_id = message.chat.id
    existing_id = _keyboard_message.get(chat_id)
 
    # Проверяем живо ли старое сообщение
    if existing_id:
        try:
            await message.bot.forward_message(
                chat_id, chat_id, existing_id
            )
            # Если дошли сюда — сообщение живо, удаляем форвард
            await message.bot.delete_message(chat_id, existing_id + 1)
            return  # клавиатура уже есть, ничего не делаем
        except Exception:
            pass  # сообщение удалено — создадим новое
 
    # Создаём новое закреплённое сообщение с клавиатурой
    # Используем символ нулевой ширины чтобы сообщение было почти невидимым
    kb_msg = await message.bot.send_message(
        chat_id,
        "⌨️",  # минимальный текст
        reply_markup=get_main_keyboard_group()
    )
    _keyboard_message[chat_id] = kb_msg.message_id

async def _send_to_dm(message: types.Message, text: str, reply_markup=None):
    """
    Отправляет ответ пользователю в личку.
    Если личка недоступна — кидает временное уведомление в группу и удаляет его.
    В любом случае удаляет исходное сообщение пользователя из группы.
    """
    dm_ok = False
    try:
        await message.bot.send_message(
            message.from_user.id,
            text,
            reply_markup=reply_markup
        )
        dm_ok = True
    except Exception:
        pass

    # Удаляем сообщение пользователя из группы
    await _delete(message)

    if not dm_ok:
        bot_info = await message.bot.get_me()
        notice = await message.answer(
            f"⚠️ @{message.from_user.username or message.from_user.first_name}, "
            f"не могу написать вам в личку. Начните диалог с ботом: "
            f"https://t.me/{bot_info.username}?start=group"
        )
        # Удаляем уведомление через 10 секунд
        await _delete(notice, delay=10)


@router.message(Command("start"))
async def start_in_group(message: types.Message):
    await _delete(message)  # удаляем /start из чата
 
    # Отправляем сообщение с клавиатурой — оно остаётся навсегда
    kb_msg = await message.bot.send_message(
        message.chat.id,
        "⌨️ Выберите действие:",
        reply_markup=get_main_keyboard_group()
    )
    _keyboard_message[message.chat.id] = kb_msg.message_id
 
    # await _send_to_dm(
    #     message,
    #     "Привет! Я бот. Используйте кнопки в группе — ответы приходят в личку."
    # )

@router.message(Command("help"))
async def help_in_group(message: types.Message):
    await _send_to_dm(
        message,
        "Доступные команды:\n/start – показать кнопки в группе\n/help – помощь"
    )


@router.message(F.text == "📩 Написать боту")
async def group_contact_bot(message: types.Message):
    bot_info = await message.bot.get_me()
    notice = await message.answer(
        f"📩 @{message.from_user.username or message.from_user.first_name}, "
        f"напишите боту в личку: https://t.me/{bot_info.username}"
    )
    await _delete(message)
    await _delete(notice, delay=10)


@router.message(F.text.in_({"🌐 Открыть сайт", "❓ Помощь", "ℹ️ О нас"}))
async def handle_group_buttons(message: types.Message):
    text = message.text

    if text == "🌐 Открыть сайт":
        await _send_to_dm(
            message,
            "Нажмите кнопку ниже, чтобы открыть сайт:",
            reply_markup=get_site_webapp_keyboard()
        )
    elif text == "❓ Помощь":
        await _send_to_dm(
            message,
            "Доступные команды:\n/start – начать работу\n/help – помощь"
        )
    elif text == "ℹ️ О нас":
        await _send_to_dm(
            message,
            "✨ О Нашем Проекте\n\n"
            "Привет! Я 🤖 Помощник, созданный, чтобы сделать ваше взаимодействие "
            "с нашим сервисом максимально удобным и быстрым.\n\n"
            "🚀 Мои возможности:\n"
            "• Мгновенный доступ к сайту — нажми на кнопку и откроется наш портал.\n"
            "• Оперативная поддержка — ответы на частые вопросы.\n"
            "• Новости и обновления — будьте в курсе всех событий.\n\n"
            "👨‍💻 О разработчике:\n"
            "Создан с ❤️ командой Urek-Mazino.\n"
            "«Мы делаем технологии ближе и понятнее»\n\n"
            "📆 Версия: 1.0.0"
        )