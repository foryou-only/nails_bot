import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, CallbackQuery
from config import BOT_TOKEN, SITE_URL
from handlers import start
from keyboards.main_keyboard import get_main_keyboard
from keyboards.webapp_keyboard import get_site_webapp_keyboard

logging.basicConfig(level=logging.INFO)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(protect_content=True)
)

dp = Dispatcher()
dp.include_router(start.router)

# Хендлер для кнопки "Старт" (исчезающая)
@dp.message(lambda message: message.text == "🚀 Старт")
async def start_button_handler(message: Message):
    await message.answer(
        "Отлично! Теперь вы можете использовать основные кнопки:",
        reply_markup=get_main_keyboard()
    )

# Хендлер для кнопки "🌐 Открыть сайт"
@dp.message(lambda message: message.text == "🌐 Открыть сайт")
async def open_site_handler(message: Message):
    await message.answer(
        "Нажмите кнопку ниже, чтобы открыть сайт в Telegram:",
        reply_markup=get_site_webapp_keyboard()
    )

# Хендлер для кнопки "❓ Помощь"
@dp.message(lambda message: message.text == "❓ Помощь")
async def help_handler(message: Message):
    await message.answer(
        "Доступные действия:\n"
        "• Открыть сайт — через Web App\n"
        "• Помощь — эта справка\n"
        "• О нас — информация о боте\n\n"
        "Если нужна помощь, обратитесь к разработчику."
    )

# Хендлер для кнопки "ℹ️ О нас"
@dp.message(lambda message: message.text == "ℹ️ О нас")
async def about_handler(message: Message):
    await message.answer(
        "Этот бот создан для демонстрации возможностей Urek-Mazino.\n"
        "Версия 1.0\n\n"
        "Автор: Urek-Mazino"
    )

# Обработка callback-запросов
@dp.callback_query()
async def callback_handler(callback: CallbackQuery):
    await callback.answer("Это демонстрационное сообщение")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен")