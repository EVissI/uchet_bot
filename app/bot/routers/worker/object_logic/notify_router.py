from aiogram import Router,F
from aiogram.types import CallbackQuery
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.bot.common.states import NotifyObjectStates
from app.bot.common.texts import get_text
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import WorkerObjectActionCallback
from app.db.dao import ObjectMemberDAO
from app.db.models import User
from app.db.database import async_session_maker

notify_worker_object = Router()


@notify_worker_object.callback_query(WorkerObjectActionCallback.filter(F.action == 'notify'), UserInfo())
async def process_notify_btn(
    callback: CallbackQuery, 
    callback_data: WorkerObjectActionCallback, 
    user_info: User,
    state: FSMContext
):
    """Handler for notification button"""
    await callback.message.delete()
    await state.update_data(object_id=callback_data.object_id)
    await state.set_state(NotifyObjectStates.waiting_message)
    
    await callback.message.answer(
        text=get_text('enter_notification', user_info.language)
    )
    


@notify_worker_object.message(F.text, StateFilter(NotifyObjectStates.waiting_message), UserInfo())
async def process_notification_message(message: Message, state: FSMContext, user_info: User):
    """Handler for processing notification message"""
    
    data = await state.get_data()
    object_id = data.get('object_id')
    
    notification_text = get_text(
        'notification_format',
        user_info.language,
        object_id=object_id,
        sender_name=user_info.user_enter_fio,
        username=f"@{user_info.username}" if user_info.username else "нет username",
        message=message.text
    )
    
    async with async_session_maker() as session:
        members = await ObjectMemberDAO.find_object_members(session, object_id)
        
        for member in members:
            if member.telegram_id != user_info.telegram_id: 
                try:
                    await message.bot.send_message(
                        chat_id=member.telegram_id,
                        text=notification_text,
                    )
                except Exception as e:
                    continue  
    
    await message.answer(
        text=get_text('notification_sent', user_info.language)
    )
    await state.clear()