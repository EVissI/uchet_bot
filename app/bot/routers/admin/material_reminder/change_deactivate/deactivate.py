from aiogram import Router, F
from aiogram.types import Message,CallbackQuery
from aiogram.filters import StateFilter

from app.bot.common.states import AdminPanelStates
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import DeleteItemConfirmCallback, ItemCardCallback, build_delete_item_confirm_kbd, build_item_card_kbd
from app.db.models import MaterialReminder, User
from app.db.database import async_session_maker
from app.db.dao import MaterialReminderDAO
from app.db.schemas import MaterialReminderFilter
from app.bot.common.texts import get_text, get_all_texts

change_reminder_router = Router()

@change_reminder_router.message(F.text.in_(get_all_texts('deactivate_reminder_btn')),StateFilter(AdminPanelStates.material_remainder_change_deactivate))
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
            text=get_text('choose_reminder_to_deactivate', user_info.language),
            reply_markup=build_item_card_kbd(
                item_id=reminder_id,
                total_pages=total_pages,
                current_page=page,
                lang=user_info.language,
                keyboard_type='deactivate_riminder'
            )
        )

@change_reminder_router.callback_query(ItemCardCallback.filter(F.keyboard_type=='deactivate_riminder',
                                                                F.action == 'deactivate'),UserInfo())
async def deactivate_reminder(callback: CallbackQuery, callback_data: ItemCardCallback, user_info: User):
    async with async_session_maker() as session:
        reminder: MaterialReminder = await MaterialReminderDAO.find_one_or_none(
            session, MaterialReminderFilter(id=callback_data.item_id)
        )
        if not reminder:
            await callback.message.answer(
                text=get_text('reminder_not_found', user_info.language)
            )
            return

        await callback.message.delete()
        await callback.message.answer(
            text=get_text('reminder_deleted_confirm', user_info.language),
            reply_markup=build_delete_item_confirm_kbd(
                item_id=reminder.id,
                lang=user_info.language,
            )
        )

@change_reminder_router.callback_query(DeleteItemConfirmCallback.filter(F.action == 'confirm'),
                                      UserInfo())
async def confirm_deactivate_reminder(callback: CallbackQuery, callback_data: DeleteItemConfirmCallback, user_info: User):
    async with async_session_maker() as session:
        reminder: MaterialReminder = await MaterialReminderDAO.find_one_or_none(
            session, MaterialReminderFilter(id=callback_data.item_id)
        )
        if not reminder:
            await callback.message.answer(
                text=get_text('reminder_not_found', user_info.language)
            )
            return

        await MaterialReminderDAO.delete(session, MaterialReminderFilter(id = reminder.id))
        await callback.message.delete()
        await callback.message.answer(
            text=get_text('reminder_deleted', user_info.language),
        )
    await callback.answer()

@change_reminder_router.callback_query(DeleteItemConfirmCallback.filter(F.action == 'cancel'),
                                      UserInfo())
async def cancel_deactivate_reminder(callback: CallbackQuery, callback_data: DeleteItemConfirmCallback, user_info: User):
    async with async_session_maker() as session:
        page, total_pages, reminder_id = await MaterialReminderDAO.find_material_reminder_by_page(
            session, callback_data.item_id + 1
        )
        if not reminder_id:
            await callback.message.answer(
                text=get_text('no_material_reminders', user_info.language)
            )
            return

        await callback.message.delete()
        await callback.message.answer(
            text=get_text('choose_reminder_to_deactivate', user_info.language),
            reply_markup=build_item_card_kbd(
                item_id=reminder_id,
                total_pages=total_pages,
                current_page=page,
                lang=user_info.language,
                keyboard_type='deactivate_riminder'
            )
        )