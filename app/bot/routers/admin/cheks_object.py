from aiogram import Router,F
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

from loguru import logger
from app.bot.common.states import AdminCheckStates
from app.bot.filters.user_info import UserInfo
from app.bot.common.texts import get_all_texts,get_text
from app.bot.kbds.inline_kbds import ObjListCallback, build_paginated_list_kbd
from app.bot.kbds.markup_kbds import MainKeyboard
from app.db.dao import ObjectCheckDAO, ObjectDAO
from app.db.models import User
from app.db.database import async_session_maker
from app.db.schemas import ObjectCheckModel, ObjectFilterModel
from app.config import settings

class SendToGroupChoise(CallbackData,prefix = 'admin_send_to_group_choise'):
    choise:str

def build_admin_reminder_send_to_group_choise(lang:str):
    kb = InlineKeyboardBuilder()
    kb.button(
        text = get_text('yes_btn', lang),
        callback_data=SendToGroupChoise(choise='yes').pack()
    )
    kb.button(
        text = get_text('no_btn', lang),
        callback_data=SendToGroupChoise(choise='no').pack()
    )
    kb.adjust(1)
    return kb.as_markup()

admin_reminder_object_router = Router()

@admin_reminder_object_router.message(F.text.in_(get_all_texts('reminder_btn')), UserInfo())
async def process_reminder_object(
    message: Message,
    state: FSMContext,
    user_info: User
):
    """Handle object selection for notification"""
    async with async_session_maker() as session:
        objects = await ObjectDAO.find_all(session, filters=ObjectFilterModel(is_active=True))
        if not objects:
            await message.answer(
                text=get_text('no_objects_found', user_info.language),
                reply_markup=MainKeyboard.build_main_kb(user_info.role, user_info.language)
            )
            return
            
        await message.answer(
            text=get_text('select_object', user_info.language),
            reply_markup=build_paginated_list_kbd(objects, context="admin_reminder_obj")
        )

@admin_reminder_object_router.callback_query(ObjListCallback.filter((F.action == 'select') &
                                                                    (F.context == 'admin_reminder_obj')),UserInfo())
async def process_admin_check_btn(
    callback: CallbackQuery,
    callback_data: ObjListCallback,
    state: FSMContext,
    user_info: User
):
    """Handler for admin check button"""
    await state.update_data(object_id=callback_data.id)
    await callback.message.delete()
    await state.set_state(AdminCheckStates.waiting_photo_and_description)
    
    await callback.message.answer(
        text=get_text('send_check_photo_and_description', user_info.language)
    )
    await callback.answer()

@admin_reminder_object_router.message(F.photo, StateFilter(AdminCheckStates.waiting_photo_and_description), UserInfo())
async def process_admin_check_description(message: Message, state: FSMContext, user_info: User):
    await state.update_data(photo_id=message.photo[-1].file_id)
    await state.update_data(description=message.caption)
    await state.set_state(AdminCheckStates.waiting_amount)
    await message.answer(
        text=get_text('enter_check_amount', user_info.language)
    )

@admin_reminder_object_router.message(F.text, StateFilter(AdminCheckStates.waiting_amount), UserInfo())
async def process_admin_check_amount(message: Message, state: FSMContext, user_info: User):
    """Handler for receiving check amount from admin"""
    try:
        amount = float(message.text.replace(',', '.'))
    except ValueError:
        await message.answer(
            text=get_text('invalid_amount', user_info.language)
        )
        return

    await state.update_data(amount=amount)
    await state.set_state(AdminCheckStates.confirm_send_to_group)
    
    await message.answer(
        text=get_text('send_to_group_question', user_info.language),
        reply_markup=build_admin_reminder_send_to_group_choise(user_info.language)
    )

@admin_reminder_object_router.callback_query(SendToGroupChoise.filter(),UserInfo())
async def process_choise(callback:CallbackQuery,callback_data:SendToGroupChoise,state:FSMContext,user_info:User):
    await callback.message.delete()
    data = await state.get_data()
    amount = data.get('amount')

    data = await state.get_data()
    async with async_session_maker() as session:
        object = await ObjectDAO.find_one_or_none(session, filters=ObjectFilterModel(id=data.get('object_id')))
    check_text = get_text(
        'check_format',
        user_info.language,
        object_name=object.name,
        worker_name=user_info.user_enter_fio,
        username=f"@{user_info.username}" if user_info.username else "нет username",
        description=data['description'],
        amount=amount
    )
    
    if callback_data.choise == 'yes':
        await callback.bot.send_photo(
            chat_id=settings.TELEGRAM_GROUP_ID_CHEKS,
            photo=data['photo_id'],
            caption=check_text,
        )
    
    async with async_session_maker() as session:
        await ObjectCheckDAO.add(
            session,
            ObjectCheckModel(
                file_id=data['photo_id'],
                description=data['description'],
                amount=amount,
                object_id=data['object_id'],
                user_id=user_info.telegram_id,
            )
        )

    await callback.message.answer(
        text=get_text('check_saved', user_info.language)
    )
    await state.clear()