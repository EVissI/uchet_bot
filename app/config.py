import os
from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from pydantic import SecretStr,PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    FORMAT_LOG: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
    LOG_ROTATION: str = "10 MB"

    BOT_TOKEN: str
    ROOT_ADMIN_IDS: List[int]

    TELEGRAM_GROUP_ID_VIDEO_OTCHET: int
    TELEGRAM_GROUP_ID_MATERIAL: int
    TELEGRAM_GROUP_ID_CHEKS: int
    TELEGRAM_GROUP_ID_OBJECT_PHOTO: int
    TELEGRAM_GROUP_ID_MATERIAL_ORDER: int
    TELEGRAM_GROUP_ID_TRANSFER_TOOL: int
    TELEGRAM_GROUP_ID_FOREMAN_REPORTS: int
    
    DB_URL: str = 'sqlite+aiosqlite:///data/db.sqlite3'

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")


settings = Settings()


bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())
admins = settings.ROOT_ADMIN_IDS

def setup_logger(app_name: str):
    
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "log")
    os.makedirs(log_dir, exist_ok=True)
    
    logger.add(
        os.path.join(log_dir, f"log_{app_name}.txt"),
        format=settings.FORMAT_LOG,
        level="INFO",
        rotation=settings.LOG_ROTATION
    )
    
    logger.add(
        os.path.join(log_dir, f"log_{app_name}_error.txt"),
        format=settings.FORMAT_LOG,
        level="ERROR",
        rotation=settings.LOG_ROTATION
    )
    