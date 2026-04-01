from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_start_keyboard():
    """Клавиатура с одной кнопкой Старт. После нажатия исчезает."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🚀 Старт")]],
        resize_keyboard=True,
        one_time_keyboard=True   # исчезает после нажатия
    )