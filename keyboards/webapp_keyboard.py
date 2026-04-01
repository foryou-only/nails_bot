from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from config import SITE_URL

def get_site_webapp_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🌐 Открыть сайт в Telegram",
                web_app=WebAppInfo(url=SITE_URL)
            )]
        ]
    )