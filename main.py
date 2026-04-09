import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from config import BOT_TOKEN
from handlers import start, group_handlers, bot_added

from keyboards.webapp_keyboard import get_site_webapp_keyboard
from config import ALLOWED_GROUP_ID
from config import GROUP_USERNAME

dp = Dispatcher()

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(protect_content=True)  # 🔒 Пункт 5: защита контента
)

async def is_user_in_allowed_group(user_id: int) -> bool:
    if ALLOWED_GROUP_ID == 0:
        return False
    try:
        member = await bot.get_chat_member(ALLOWED_GROUP_ID, user_id)
        return member.status not in ["left", "kicked"]
    except:
        return False
    
logging.basicConfig(level=logging.INFO)




# Подключаем роутеры
dp.include_router(start.router)           # Для личных сообщений
dp.include_router(group_handlers.router)   # Для групповых сообщений
dp.include_router(bot_added.router)        # Для добавления бота в группу

# Обработчики для личного чата
@dp.message(lambda msg: msg.text == "🌐 Открыть сайт" and msg.chat.type == "private")
async def private_open_site(message: Message):
    if not await is_user_in_allowed_group(message.from_user.id):
            await message.answer("❌ Доступ только участникам группы.")
            return
    await message.answer(
        "Нажмите кнопку, чтобы открыть сайт:",
        reply_markup=get_site_webapp_keyboard()
    )
# async def private_open_site(message: Message):
#     await message.answer(
#         "Нажмите кнопку, чтобы открыть сайт:",
#         reply_markup=get_site_webapp_keyboard()
#     )

@dp.message(lambda msg: msg.text == "❓ Помощь" and msg.chat.type == "private")
async def private_help(message: Message):
    await message.answer(
        "Доступные команды:\n"
        "/start - начать работу\n"
        # "/help - получить помощь\n\n"
        "Используйте кнопки под полем ввода для навигации."
    )

@dp.message(lambda msg: msg.text == "ℹ️ О нас" and msg.chat.type == "private")
async def private_about(message: Message):
    await message.answer(
        "Этот бот создан для удобного взаимодействия с нашим сервисом.\n"
        "Версия 1.0\n\n"
    )

@dp.message(lambda msg: msg.text == "👥 Перейти в группу" )
async def private_group_link(message: Message):
    if GROUP_USERNAME:
        await message.answer(f"👥 Вот ссылка на нашу группу: {GROUP_USERNAME}")
    else:
        await message.answer("Ссылка на группу пока не настроена. Обратитесь к администратору.")
async def main():
    await dp.start_polling(bot)
 

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен")

       


    
