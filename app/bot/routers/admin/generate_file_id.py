﻿from aiogram import Router,F
from aiogram.filters import StateFilter
from aiogram.types import Message
from loguru import logger
from app.bot.common.states import AdminPanelStates
from app.bot.common.texts import get_text
from app.bot.filters.user_info import UserInfo
from app.db.models import User

generate_file_id_router = Router()

@generate_file_id_router.message(F.photo,StateFilter(None, AdminPanelStates),UserInfo())
async def process_photo_for_file_id(message: Message, user_info: User):
    """Generate and return file_id from photo"""
    try:
        file_id = message.photo[-1].file_id
        logger.info(f"Generated file_id for user {user_info.telegram_id}: {file_id}")
        
        await message.reply(
            text=get_text(
                "file_id_generated",
                user_info.language,
                file_id=f"`{file_id}`"
            ),
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Error generating file_id for user {user_info.telegram_id}: {e}")
        await message.reply(
            text=get_text("file_id_generation_error", user_info.language)
        )

@generate_file_id_router.message(F.text.regexp(r"^[A-Za-z0-9_-]{20,}$"), StateFilter(None, AdminPanelStates), UserInfo())
async def process_file_id_as_text(message: Message, user_info: User):
    """Отправить фото по file_id, если пользователь прислал file_id текстом"""
    file_id = message.text.strip()
    try:
        try:
            await message.reply_photo(
                photo=file_id,
                parse_mode="Markdown"
            )
        except:
            await message.reply_document(
                document=file_id,
                parse_mode="Markdown"
            )
    except Exception as e:
        logger.error(f"Error sending photo by file_id for user {user_info.telegram_id}: {e}")
        await message.reply(
            text=get_text("file_id_generation_error", user_info.language)
        )