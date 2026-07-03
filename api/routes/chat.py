from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.llm import get_ai_response
from core.models import User, Character, Dialog, Message
from api.schemas import ChatRequest, ChatResponse
from core.character_prompts import CHARACTER_PROMPTS

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/send", response_model=ChatResponse)
def send_message(req: ChatRequest, db: Session = Depends(get_db)):
    # 1. Находим или создаём пользователя
    user = db.query(User).filter(User.telegram_id == req.user_id).first()
    if not user:
        user = User(telegram_id=req.user_id)
        db.add(user)
        db.commit()
    
    # 2. Находим персонажа в БД (или берём из CHARACTER_PROMPTS)
    char = db.query(Character).filter(Character.char_id == req.character_id).first()
    if not char:
        # Если нет в БД — берём из словаря промптов
        if req.character_id in CHARACTER_PROMPTS:
            cp = CHARACTER_PROMPTS[req.character_id]
            char = Character(
                char_id=req.character_id,
                name=cp["name"],
                description=cp["description"],
                tags=cp["tags"],
                avatar_url=cp["avatar_url"],
                system_prompt=cp["system_prompt"]
            )
            db.add(char)
            db.commit()
        else:
            return ChatResponse(reply="Персонаж не найден", character_name="Система")
    
    # 3. Находим или создаём диалог
    dialog = db.query(Dialog).filter(
        Dialog.user_id == user.id,
        Dialog.character_id == char.id
    ).first()
    if not dialog:
        dialog = Dialog(user_id=user.id, character_id=char.id)
        db.add(dialog)
        db.commit()
    
    # 4. Собираем историю
    history = []
    for msg in dialog.messages[-20:]:  # последние 20 сообщений
        history.append({"role": msg.role, "content": msg.content})
    
    # 5. Получаем ответ от ИИ
    reply_text = get_ai_response(char.system_prompt, history, req.message)
    
    # 6. Сохраняем сообщения в БД
    user_msg = Message(dialog_id=dialog.id, role="user", content=req.message)
    ai_msg = Message(dialog_id=dialog.id, role="assistant", content=reply_text)
    db.add(user_msg)
    db.add(ai_msg)
    db.commit()
    
    return ChatResponse(reply=reply_text, character_name=char.name)