import asyncio
import uvicorn
from multiprocessing import Process

def run_api():
    """Запуск FastAPI"""
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=False)

def run_bot():
    """Запуск Telegram бота"""
    from bot.main import main
    asyncio.run(main())

if __name__ == "__main__":
    print("=" * 40)
    print("🚀 AnyChars запускается...")
    print("=" * 40)
    
    # Запускаем API в отдельном процессе
    api_process = Process(target=run_api)
    api_process.start()
    
    print("📡 API: http://localhost:8000")
    print("🤖 Бот запускается...")
    
    # Бота запускаем в основном процессе
    run_bot()
    
    api_process.join()