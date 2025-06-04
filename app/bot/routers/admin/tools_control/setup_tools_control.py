from aiogram import Router,F
from aiogram.types import Message
from aiogram.fsm.context import  FSMContext
from aiogram.filters import StateFilter
from app.bot.common.states import AdminPanelStates
from app.bot.common.texts import get_all_texts,get_text
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.markup_kbds import AdminToolsControlKeyboard,MainKeyboard
from app.db.models import User

setup_tools_control_router = Router()

@setup_tools_control_router.message(F.text.in_(get_all_texts('instrument_control_btn')),UserInfo())
async def create_tool_control_kbd(message:Message, state:FSMContext, user_info:User):
    await message.delete()
    await message.answer(message.text,
                         reply_markup=AdminToolsControlKeyboard.build_tool_control_kb(lang=user_info.language))
    await state.set_state(AdminPanelStates.tools_control)


@setup_tools_control_router.message(F.text.in_(get_all_texts('back_btn')),
                            StateFilter(AdminPanelStates.tools_control),
                            UserInfo())
async def process_back_btn(message:Message,state:FSMContext,user_info:User):
    await message.delete()
    await message.answer(message.text,
                         reply_markup=MainKeyboard.build_main_kb(lang=user_info.language,role=user_info.role))
    await state.clear()