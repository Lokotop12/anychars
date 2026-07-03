import httpx
from groq import Groq
from core.config import settings

# Создаём клиент с принудительно пустыми настройками прокси
http_client = httpx.Client(
    transport=httpx.HTTPTransport(proxy=None),
    mounts={"all://": httpx.HTTPTransport(proxy=None)}
)

client = Groq(
    api_key=settings.GROQ_API_KEY,
    http_client=http_client
)

MODEL = "llama-3.3-70b-versatile"

def get_ai_response(system_prompt: str, history: list, user_message: str) -> str:
    messages = [{"role": "system", "content": system_prompt}]

    for msg in history[-20:]:
        messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.85,
            max_tokens=200,
            top_p=0.95
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"Groq Error: {e}")
        return "*молчание*... Кажется, связь с духами прервалась. Попробуй ещё раз."