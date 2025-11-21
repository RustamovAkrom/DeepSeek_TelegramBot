from aiogram.types import Message


async def split_text_for_telegram(text: str, chunk_size: int = 4000):
    for i in range(0, len(text), chunk_size):
        yield text[i: i + chunk_size]


async def send_long(message: Message, text: str, markup=None):
    MAX_LEN = 4000
    for i in range(0, len(text), MAX_LEN):
        await message.answer(text[i:i+MAX_LEN], reply_markup=markup if i == 0 else None)
