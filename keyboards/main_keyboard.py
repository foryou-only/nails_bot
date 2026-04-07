from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard_group():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌐 Открыть сайт")],
            [KeyboardButton(text="❓ Помощь"), KeyboardButton(text="ℹ️ О нас")],
            [KeyboardButton(text="📩 Написать боту")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🌐 Открыть сайт")],
            [KeyboardButton(text="❓ Помощь"), KeyboardButton(text="ℹ️ О нас")],
            [KeyboardButton(text="👥 Перейти в группу")]   
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )

