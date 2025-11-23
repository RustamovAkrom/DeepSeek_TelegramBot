import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config import settings
from app.handlers.admin import router as admin_router
from app.handlers.start import router as start_router
from app.handlers.user_profile import router as user_profile_router
from app.handlers.ai_chat import router as ai_chat_router
from app.handlers.ai_models import router as ai_models_router
from app.handlers.help import router as help_router
from app.db.base import engine, Base


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="Show help information"),
        BotCommand(command="admin", description="Admin panel"),
        BotCommand(command="models", description="Change DeepSeek model"),
        BotCommand(command="profile", description="Your profile"),
    ]
    await bot.set_my_commands(commands)


async def main():
    # Initialize database
    await init_db()

    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()

    # Add commands menu
    await set_commands(bot)

    # Register routers from handlers
    dp.include_router(start_router)
    dp.include_router(admin_router)
    dp.include_router(user_profile_router)
    dp.include_router(help_router)
    dp.include_router(ai_models_router)
    dp.include_router(ai_chat_router)  # It must be last

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped")
