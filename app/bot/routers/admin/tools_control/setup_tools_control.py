from aiogram import Router,F
from aiogram.types import Message
from aiogram.fsm.context import  FSMContext
from aiogram.filters import StateFilter
from app.bot.common.states import AdminPanelStates
from app.bot.common.texts import get_all_texts,get_text
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.markup_kbds import AdminToolsControlKeyboard,MainKeyboard

from app.bot.routers.admin.tools_control.bulk_transfer_tool import bulk_transfer_router
from app.bot.routers.admin.tools_control.tmc import tmc_router
from app.bot.routers.admin.tools_control.tools_export import tools_export_router
from app.bot.routers.admin.tools_control.users_tools_xlsx import users_tools_xlsx_router
from app.db.models import User

setup_tools_control_router = Router()
setup_tools_control_router.include_routers(
    bulk_transfer_router,
    tmc_router,
    tools_export_router,
    users_tools_xlsx_router
)

@setup_tools_control_router.message(F.text.in_(get_all_texts('instrument_control_btn')),
                                    StateFilter(None),
                                    UserInfo())
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