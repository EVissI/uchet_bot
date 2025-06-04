from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, BufferedInputFile
from loguru import logger
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
import io

from app.bot.common.excel.utils import create_materials_excel
from app.bot.common.states import AdminPanelStates
from app.bot.common.texts import get_all_texts, get_text
from app.bot.filters.user_info import UserInfo
from app.db.dao import MaterialReminderDAO
from app.db.models import User
from app.db.database import async_session_maker

material_reminder_excel_view_router = Router()


@material_reminder_excel_view_router.message(
    F.text.in_(get_all_texts("materials_excel_btn")),
    StateFilter(AdminPanelStates.material_remainder_control),
    UserInfo()
)
async def process_materials_excel(message: Message, user_info: User):
    """Handle materials excel export button"""
    try:
        logger.info(f"User {user_info.telegram_id} requested materials excel export")
        
        async with async_session_maker() as session:
            materials = await MaterialReminderDAO.find_all(session)
            
            if not materials:
                await message.answer(get_text("no_materials_found", user_info.language))
                return

            excel_file = await create_materials_excel(materials, user_info.language)
            
            await message.answer_document(
                document=BufferedInputFile(
                    excel_file.getvalue(),
                    filename=f"materials_{message.date.strftime('%d_%m_%Y')}.xlsx"
                ),
                caption=get_text(
                    "materials_export_complete",
                    user_info.language,
                    count=len(materials)
                )
            )
            logger.info(f"Materials excel exported successfully for user {user_info.telegram_id}")
            
    except Exception as e:
        logger.error(f"Error exporting materials excel for user {user_info.telegram_id}: {e}")
        await message.answer(get_text("materials_export_error", user_info.language))