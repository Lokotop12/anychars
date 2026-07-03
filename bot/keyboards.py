from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from core.config import settings

def get_start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🎭 Открыть каталог персонажей",
                web_app=WebAppInfo(url=settings.MINI_APP_URL)
            )
        ],
        [
            InlineKeyboardButton(
                text="💬 Быстрый чат с Юки",
                callback_data="quick_chat_yuki"
            )
        ],
        [
            InlineKeyboardButton(
                text="💬 Быстрый чат с Рексом",
                callback_data="quick_chat_rex"
            )
        ]
    ])

def get_back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ В каталог", callback_data="back_to_catalog")]
    ])