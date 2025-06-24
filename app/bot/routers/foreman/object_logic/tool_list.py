from datetime import datetime
from aiogram import Router, F
from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.bot.common.texts import get_text
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import (
    ForemanObjectCallback,
    get_tool_status_kbd,
    ForemanToolStatusCallback
)
from app.db.dao import ToolDAO
from app.db.models import User, Tool
from app.db.database import async_session_maker
from app.bot.common.excel.utils import create_tools_export, create_tools_report

tools_list_router = Router()

@tools_list_router.callback_query(
    ForemanObjectCallback.filter(F.action == "tools_list"), 
    UserInfo()
)
async def process_tools_list_btn(
    callback: CallbackQuery,
    callback_data: ForemanObjectCallback,
    state: FSMContext,
    user_info: User
) -> None:
    """Initial handler for tools list button"""
    await callback.message.delete()
    await callback.message.answer(
        text=get_text("select_tool_status", user_info.language),
        reply_markup=get_tool_status_kbd(user_info.language)
    )


@tools_list_router.callback_query(ForemanToolStatusCallback.filter(), UserInfo())
async def process_tool_status(
    callback: CallbackQuery,
    callback_data: ForemanToolStatusCallback,
    state: FSMContext,
    user_info: User
) -> None:
    """Handler for tool status selection"""
    async with async_session_maker() as session:
        tools = await ToolDAO.get_filtered_tools(
            session,
            status=callback_data.status
        )
        
        if not tools:
            await callback.message.edit_text(
                text=get_text("no_tools_found", user_info.language)
            )
            return

        excel_file = create_tools_export(tools, user_info.language)
        
        input_file = BufferedInputFile(
            excel_file.getvalue(),
            filename=f"tools_report_{datetime.now().strftime('%d_%m_%Y')}.xlsx"
        )
        
        await callback.message.delete()
        await callback.message.answer_document(
            document=input_file,
            caption=get_text(
                "tools_list_caption",
                user_info.language,
                tool_status=callback_data.status
            )
        )