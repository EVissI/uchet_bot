from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter

from app.bot.common.states import AdminPanelStates
from app.bot.kbds.inline_kbds import build_item_card_kbd
from app.db.models import User
from app.db.database import async_session_maker
from app.db.dao import MaterialReminderDAO
from app.db.schemas import MaterialReminderFilter
from app.bot.common.texts import get_text, get_all_texts

change_reminder_router = Router()

@change_reminder_router.message(F.text.in_(get_all_texts('change_reminder_btn')),StateFilter(AdminPanelStates.material_remainder_change_deactivate))
async def change_reminder(message: Message, user_info: User):
    async with async_session_maker() as session:
        page, total_pages, reminder_id = await MaterialReminderDAO.find_material_reminder_by_page(
            session, 1
        )
        if not reminder_id:
            await message.answer(
                text=get_text('no_material_reminders', user_info.language)
            )
            return
        await message.answer(
            text=message.text,
            reply_markup=build_item_card_kbd(
                item_id=reminder_id,
                total_pages=total_pages,
                current_page=page,
                lang=user_info.language,
                keyboard_type='change_order_riminder'
            )
        )

