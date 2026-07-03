from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, index=True)  # ID в Telegram
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Связи
    dialogs = relationship("Dialog", back_populates="user")

class Character(Base):
    __tablename__ = "characters"
    
    id = Column(Integer, primary_key=True)
    char_id = Column(String, unique=True, index=True)  # "yuki", "rex"
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    tags = Column(String, nullable=True)  # "дух, снег, поэзия"
    avatar_url = Column(String, nullable=True)
    system_prompt = Column(Text, nullable=False)  # промпт личности
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Dialog(Base):
    __tablename__ = "dialogs"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    character_id = Column(Integer, ForeignKey("characters.id"))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    user = relationship("User", back_populates="dialogs")
    character = relationship("Character")
    messages = relationship("Message", back_populates="dialog", order_by="Message.created_at")

class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True)
    dialog_id = Column(Integer, ForeignKey("dialogs.id"))
    role = Column(String)  # "user" или "assistant"
    content = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    dialog = relationship("Dialog", back_populates="messages")