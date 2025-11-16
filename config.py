from pydantic_settings import BaseSettings
from pydantic import validator
from typing import List, Union


class Settings(BaseSettings):
    DEEPSEEK_API_KEY: str
    DEFAULT_MODEL: str = "deepseek/deepseek-chat-v3-0324"

    TELEGRAM_BOT_TOKEN: str
    ADMIN_IDS: list[int] = []

    DATABASE_URL: str
    TEST_DATABASE_URL: str = "sqlite+aiosqlite:///./data.db"
    
    ENV: str = "dev" # "dev" or "prod"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    
    @property
    def current_database_url(self) -> str:
        """Возвращает URL базы для текущего ENV."""
        return self.DATABASE_URL if self.ENV == "prod" else self.TEST_DATABASE_URL

    @validator("ADMIN_IDS", pre=True)
    def parse_admin_ids(cls, v: Union[str, int, list]):
        if isinstance(v, int):
            return [v]
        if isinstance(v, str):
            return [int(x.strip()) for x in v.split(",") if x.strip()]
        return v


settings = Settings()

# import os
# from typing import List
# from dotenv import load_dotenv

# load_dotenv()

# DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
# TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data.db")

# ADMIN_IDS: List[int] = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

# DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "deepseek/deepseek-chat-v3-0324")
