from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from core.models import Character
from api.schemas import CharacterCard
from core.character_prompts import CHARACTER_PROMPTS

router = APIRouter(prefix="/characters", tags=["characters"])

@router.get("/list", response_model=list[CharacterCard])
def list_characters(db: Session = Depends(get_db)):
    chars = db.query(Character).filter(Character.is_active == True).all()
    
    # Если БД пустая — отдаём из словаря
    if not chars:
        result = []
        for char_id, cp in CHARACTER_PROMPTS.items():
            result.append(CharacterCard(
                id=char_id,
                name=cp["name"],
                description=cp["description"],
                tags=cp["tags"],
                avatar_url=cp["avatar_url"],
                is_active=True
            ))
        return result
    
    return [
        CharacterCard(
            id=c.char_id,
            name=c.name,
            description=c.description or "",
            tags=c.tags or "",
            avatar_url=c.avatar_url,
            is_active=c.is_active
        )
        for c in chars
    ]