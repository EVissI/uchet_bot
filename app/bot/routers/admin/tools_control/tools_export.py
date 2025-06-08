import io
from datetime import datetime
from loguru import logger
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, BufferedInputFile

from app.bot.common.excel.utils import create_tools_export
from app.bot.common.states import AdminPanelStates
from app.bot.common.texts import get_text, get_all_texts
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import get_tools_status_export_kbd, ToolStatusCallback
from app.db.dao import ToolDAO
from app.db.models import User
from app.db.database import async_session_maker


tools_export_router = Router()

@tools_export_router.message(
    F.text.in_(get_all_texts("tools_export_btn")),
    StateFilter(AdminPanelStates.tools_control),
    UserInfo()
)
async def process_tools_export_btn(message: Message, user_info: User):
    """Handle tools export button"""
    logger.info(f"User {user_info.telegram_id} requested tools export")
    await message.answer(
        text=get_text("select_tools_status", user_info.language),
        reply_markup=get_tools_status_export_kbd(user_info.language)
    )

@tools_export_router.callback_query(ToolStatusCallback.filter())
async def process_tools_export(callback: CallbackQuery, callback_data: ToolStatusCallback, user_info: User):
    """Handle tools export by status"""
    logger.info(f"User {user_info.telegram_id} exporting tools with status: {callback_data.status}")
    
    try:
        async with async_session_maker() as session:
            if callback_data.status == "all":
                tools = await ToolDAO.find_all(session)
            else:
                tools = await ToolDAO.get_filtered_tools(session, callback_data.status)

            if not tools:
                await callback.message.edit_text(get_text("no_tools_found", user_info.language))
                return

            excel_file = create_tools_export(tools, user_info.language)
            
            filename = f"tools_export_{callback_data.status}_{datetime.now().strftime('%d_%m_%Y')}.xlsx"
            
            await callback.message.answer_document(
                document=BufferedInputFile(
                    excel_file.getvalue(),
                    filename=filename
                ),
                caption=get_text(
                    "tools_export_complete",
                    user_info.language,
                    status=get_text(f"tool_status_{callback_data.status}", user_info.language),
                    count=len(tools)
                )
            )
            await callback.message.delete()
            
    except Exception as e:
        logger.error(f"Error exporting tools for user {user_info.telegram_id}: {e}")
        await callback.message.edit_text(
            get_text("tools_export_error", user_info.language)
        )