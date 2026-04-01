from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌐 Открыть сайт")],
            [KeyboardButton(text="❓ Помощь"), KeyboardButton(text="ℹ️ О нас")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )