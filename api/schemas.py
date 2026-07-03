from pydantic import BaseModel
from typing import Optional

# Запрос: пользователь отправляет сообщение
class ChatRequest(BaseModel):
    user_id: int
    character_id: str
    message: str

# Ответ: что вернул ИИ
class ChatResponse(BaseModel):
    reply: str
    character_name: str

# Карточка персонажа для каталога
class CharacterCard(BaseModel):
    id: str
    name: str
    description: str
    tags: str
    avatar_url: Optional[str] = None
    is_active: bool

# Запрос на создание персонажа
class CharacterCreate(BaseModel):
    char_id: str
    name: str
    description: str
    tags: str
    avatar_url: Optional[str] = None
    system_prompt: str