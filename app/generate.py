import requests
import os
import json

from openai import AsyncOpenAI

from config import DEEPSEEK_API_KEY


client = AsyncOpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=DEEPSEEK_API_KEY,
)

async def ai_generate(text: str, model: str = "deepseek/deepseek-chat-v3-0324"):
  completion = await client.chat.completions.create(
    model=model,
    messages=[
                {
                  "role": "user",
                  "content": text
                }
              ]
  )
  print(completion)
  return completion.choices[0].message.content
