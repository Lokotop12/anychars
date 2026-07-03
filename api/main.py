from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import chat, characters
from core.database import init_db
from core.config import settings

app = FastAPI(title="AnyChars API", version="0.1.0")

# CORS — разрешаем запросы от Mini App
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.MINI_APP_URL, "https://web.telegram.org"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
app.include_router(characters.router)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/")
def root():
    return {"message": "AnyChars API работает"}