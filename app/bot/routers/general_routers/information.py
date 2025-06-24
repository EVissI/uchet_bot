from aiogram import Router, F
from aiogram.types import Message


from app.bot.common.texts import get_all_texts,get_text
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import inforamtion_buttons
from app.db.models import User

information_router = Router()

@information_router.message(F.text.in_(get_all_texts("info_btn")), UserInfo())
async def info_cmd(message:Message, user_info:User):
    await message.answer(text=get_text("pass",user_info.language),
                        reply_markup=inforamtion_buttons())