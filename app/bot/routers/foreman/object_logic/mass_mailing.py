from loguru import logger

from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.bot.common.texts import get_text
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import ForemanObjectCallback
from app.db.dao import ObjectDAO, ObjectDocumentDAO
from app.db.models import User, ObjectDocument,Object
from app.db.database import async_session_maker

mass_mailing_router = Router()