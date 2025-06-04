from aiogram import Router,F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.bot.common.texts import get_text, get_all_texts
from app.bot.kbds.markup_kbds import AdminMaterialReminderKeyboard,MainKeyboard
from app.bot.filters.user_info import UserInfo
from app.db.models import User
from app.bot.common.states import AdminPanelStates

from app.bot.routers.admin.material_reminder.excel_view import material_reminder_excel_view_router
from app.bot.routers.admin.material_reminder.change_deactivate.setup import setup_activate_deactivate_reminder_router

reminder_setup_router = Router()
reminder_setup_router.include_routers(
    material_reminder_excel_view_router,
    setup_activate_deactivate_reminder_router
)

@reminder_setup_router.message(F.text.in_(get_all_texts("reminder_setup_btn")),StateFilter(None),UserInfo())
async def create_material_reminder_kb(message: Message, state:FSMContext,user_info: User):
    await state.set_state(AdminPanelStates.material_remainder_control)
    await message.answer(
        text=message.text,
        reply_markup=AdminMaterialReminderKeyboard.get_material_reminder_setup_kb(user_info.language)
    )

@reminder_setup_router.message(F.text.in_(get_all_texts("back_btn")),StateFilter(AdminPanelStates.material_remainder_control),UserInfo())
async def back_to_admin_panel(message: Message, state:FSMContext,user_info: User):
    await state.clear()
    await message.answer(
        text=message.text,
        reply_markup=MainKeyboard.build_main_kb(user_info.role, user_info.language)
    )