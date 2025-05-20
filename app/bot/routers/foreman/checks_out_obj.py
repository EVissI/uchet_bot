from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.bot.filters.user_info import UserInfo
from app.bot.common.texts import get_text
from app.config import settings

checks_out_object_router = Router()

