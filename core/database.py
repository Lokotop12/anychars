from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from core.config import settings

# create_engine — точка входа в БД
engine = create_engine(settings.DATABASE_URL, echo=False)

# SessionLocal — фабрика сессий (каждый запрос получает свою сессию)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Base — родитель для всех моделей таблиц
class Base(DeclarativeBase):
    pass

def get_db():
    """Генератор сессий для FastAPI (отдаёт сессию и закрывает после запроса)"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Создаёт все таблицы (вызывается при старте)"""
    Base.metadata.create_all(bind=engine)