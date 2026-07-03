import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    MINI_APP_URL: str = os.getenv("MINI_APP_URL", "https://miniapp-seven-omega.vercel.app")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///anychars.db")

settings = Settings()