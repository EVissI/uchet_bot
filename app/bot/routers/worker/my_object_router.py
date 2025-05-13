from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from app.bot.common.texts import get_all_texts, get_text
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import object_keyboard
from app.db.dao import ObjectMemberDAO
from app.db.database import async_session_maker
from app.db.models import User

my_object_router = Router()

@my_object_router.message(F.text.in_(get_all_texts('my_objects_btn')), UserInfo())
async def process_my_objects(message: Message, user_info: User):
    """Handler for displaying user's objects"""
    
    async with async_session_maker() as session:
        objects = await ObjectMemberDAO.find_user_objects(session, user_info.telegram_id)
        
        if not objects:
            await message.answer(
                get_text('no_objects', user_info.language)
            )
            return
        
        
        for obj in objects:
            object_text = get_text(
                'object_item',
                user_info.language,
                name=obj.name,
                description=obj.description or get_text('no_description', user_info.language)
            )
            
            await message.answer(
                text=object_text,
                parse_mode="MarkdownV2",
                reply_markup=object_keyboard(obj.id, user_info.language)
            )
    
