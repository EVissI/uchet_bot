from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from app.bot.common.states import AdminPanelStates
from app.bot.common.texts import get_text, get_all_texts
from app.bot.filters.role_filter import RoleFilter
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.markup_kbds import AdminObjectControlKeyboard,MainKeyboard
from app.bot.routers.general_routers.object_control.create_object_router import create_object_router
from app.bot.routers.general_routers.object_control.add_member_to_object import add_member_to_object_router
from app.bot.routers.general_routers.object_control.delete_object import delete_object_router
from app.db.models import User


setup_object_control_router = Router()
setup_object_control_router.message.filter(RoleFilter([User.Role.admin.value,
                                          User.Role.foreman.value,
                                          User.Role.buyer.value]))

setup_object_control_router.include_routers(
    create_object_router,
    add_member_to_object_router,
    delete_object_router
)

@setup_object_control_router.message(F.text.in_(get_all_texts('object_control_btn')),UserInfo())
async def process_object_control(message: Message,state:FSMContext, user_info: User):
    """Handler for displaying object control options"""
    await message.delete()
    await message.answer(
        text=message.text,
        reply_markup=AdminObjectControlKeyboard.build_object_control_kb(user_info.language)
    )
    await state.set_state(AdminPanelStates.objects_control)

@setup_object_control_router.message(F.text == get_text('back_btn'),StateFilter(AdminPanelStates.objects_control), UserInfo())
async def process_back_btn(message: Message,state:FSMContext, user_info: User):
    """Handler for back button in object control"""
    await message.delete()
    await message.answer(
        text=message.text,
        reply_markup=MainKeyboard.build_main_kb(user_info.role, user_info.language)
    )
    await state.clear()