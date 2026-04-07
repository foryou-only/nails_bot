from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from config import SITE_URL

def get_site_webapp_keyboard():
    """Создает inline-кнопку для открытия сайта внутри Telegram."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🌐 Открыть сайт",
                web_app=WebAppInfo(url=SITE_URL)
            )]
        ]
    )