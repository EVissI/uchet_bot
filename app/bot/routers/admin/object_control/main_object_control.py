from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from app.bot.common.states import AdminPanelStates
from app.bot.common.texts import get_text, get_all_texts
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.markup_kbds import AdminObjectControlKeyboard,MainKeyboard
from app.bot.routers.admin.object_control.create_object_router import create_object_router
from app.db.models import User


main_object_control_router = Router()
main_object_control_router.include_routers(
    create_object_router
)

@main_object_control_router.message(F.text.in_(get_all_texts('object_control_btn')),UserInfo())
async def process_object_control(message: Message,state:FSMContext, user_info: User):
    """Handler for displaying object control options"""
    await message.answer(
        text=message.text,
        reply_markup=AdminObjectControlKeyboard.build_object_control_kb(user_info.language)
    )
    await state.set_state(AdminPanelStates.objects_control)

@main_object_control_router.message(F.text == get_text('back_btn'), UserInfo(),StateFilter(AdminObjectControlKeyboard))
async def process_back_btn(message: Message,state:FSMContext, user_info: User):
    """Handler for back button in object control"""
    await message.answer(
        text=message.text,
        reply_markup=MainKeyboard.build_main_kb(user_info.role, user_info.language)
    )
    await state.clear()