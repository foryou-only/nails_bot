from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_start_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🚀 Start")]],
        resize_keyboard=True,
        one_time_keyboard=False   # не исчезает после нажатия, но мы удалим сообщение вручную
    )

def get_start_keyboard_group():
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🚀 Start")]],
        resize_keyboard=True,
        one_time_keyboard=False   # не исчезает после нажатия, но мы удалим сообщение вручную
    )