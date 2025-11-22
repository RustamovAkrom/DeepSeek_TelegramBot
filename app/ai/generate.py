from typing import Optional, List, Dict
from openai import AsyncOpenAI
from config import settings


def get_client(api_key: Optional[str] = None) -> AsyncOpenAI:
    return AsyncOpenAI(
        api_key=api_key or settings.DEEPSEEK_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )


async def ai_generate(
    text: str,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    message: Optional[List[Dict]] = None,
) -> str:
    """
    Генерация текста через OpenRouter / DeepSeek.

    Args:
        text: сообщение пользователя
        model: модель для генерации (по умолчанию settings.DEFAULT_MODEL)
        api_key: свой ключ для override (если нужно)
        messages: контекст сообщений, например [{"role": "user", "content": "..."}]

    Returns:
        Сгенерированный текст AI
    """
    model = model or settings.DEFAULT_MODEL
    message = message or [{"role": "user", "content": text}]

    client = get_client(api_key=api_key)

    completion = await client.chat.completions.create(model=model, message=message)

    return completion.choices[0].message.content
