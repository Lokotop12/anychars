from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from core.llm import get_ai_response
from core.character_prompts import CHARACTER_PROMPTS
from bot.keyboards import get_start_keyboard, get_back_keyboard

router = Router()

# Временное хранилище состояний (потом заменим на Redis)
user_states = {}  # {user_id: character_id}
user_dialogs = {} # {user_id: {char_id: [messages]}}

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "🎭 Добро пожаловать в <b>AnyChars</b>!\n\n"
        "Выбери персонажа и начни общение:",
        reply_markup=get_start_keyboard(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "quick_chat_yuki")
@router.callback_query(F.data == "quick_chat_rex")
async def quick_chat_rex(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_states[user_id] = "rex"
    await callback.message.edit_text(
        "🐺 Ты общаешься с <b>Рексом</b>. Напиши что-нибудь...\n"
        "/reset — очистить историю\n"
        "/stop — закончить чат",
        parse_mode="HTML",
        reply_markup=get_back_keyboard()
    )
    await callback.answer()
async def quick_chat_yuki(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_states[user_id] = "yuki"
    await callback.message.edit_text(
        "❄️ Ты общаешься с <b>Юки-онной</b>. Напиши что-нибудь...\n"
        "/reset — очистить историю\n"
        "/stop — закончить чат",
        parse_mode="HTML",
        reply_markup=get_back_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "back_to_catalog")
async def back_to_catalog(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in user_states:
        del user_states[user_id]
    await callback.message.edit_text(
        "🎭 Выбери персонажа:",
        reply_markup=get_start_keyboard()
    )
    await callback.answer()

@router.message(Command("reset"))
async def cmd_reset(message: Message):
    user_id = message.from_user.id
    if user_id in user_states:
        char_id = user_states[user_id]
        if user_id in user_dialogs and char_id in user_dialogs[user_id]:
            user_dialogs[user_id][char_id] = []
        await message.answer("🔄 История диалога очищена.")
    else:
        await message.answer("Сначала выбери персонажа: /start")

@router.message(Command("stop"))
async def cmd_stop(message: Message):
    user_id = message.from_user.id
    if user_id in user_states:
        del user_states[user_id]
    await message.answer("Чат завершён. /start — выбрать нового персонажа")

@router.message(F.text & ~F.text.startswith("/"))
async def handle_chat(message: Message):
    user_id = message.from_user.id
    
    if user_id not in user_states:
        await message.answer("Сначала выбери персонажа: /start")
        return
    
    char_id = user_states[user_id]
    if char_id not in CHARACTER_PROMPTS:
        await message.answer("Персонаж не найден. /start")
        return
    
    char = CHARACTER_PROMPTS[char_id]
    
    # Инициализируем историю
    if user_id not in user_dialogs:
        user_dialogs[user_id] = {}
    if char_id not in user_dialogs[user_id]:
        user_dialogs[user_id][char_id] = []
    
    history = user_dialogs[user_id][char_id]
    
    # Отправляем "печатает..."
    await message.bot.send_chat_action(message.chat.id, "typing")
    
    # Получаем ответ от ИИ
    reply = get_ai_response(char["system_prompt"], history, message.text)
    
    # Сохраняем в историю
    history.append({"role": "user", "content": message.text})
    history.append({"role": "assistant", "content": reply})
    user_dialogs[user_id][char_id] = history[-20:]  # держим 20 сообщений
    
    await message.answer(reply)