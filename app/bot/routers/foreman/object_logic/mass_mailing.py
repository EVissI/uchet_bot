from loguru import logger

from aiogram import Router, F
from aiogram.types import CallbackQuery,Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.bot.common.states import NotifyObjectStates
from app.bot.common.texts import get_text
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import ForemanObjectCallback, get_back_kbd
from app.db.dao import ObjectMemberDAO
from app.db.models import User
from app.db.database import async_session_maker

mass_mailing_router = Router()


@mass_mailing_router.callback_query(ForemanObjectCallback.filter(F.action == "mass_mailing"), UserInfo())
async def handle_mass_mailing(callback: CallbackQuery, callback_data: ForemanObjectCallback, state:FSMContext, user_info: User) -> None:
    """Обработчик для кнопки массовой рассылки"""
    await callback.message.delete()
    last_message = await callback.answer(get_text("enter_notification", user_info.language),
                          reply_markup=get_back_kbd(user_info.language, callback_data.object_id))
    await state.update_data(last_senden_msg_id=last_message.message_id)
    await state.update_data(object_id=callback_data.object_id)
    await state.set_state(NotifyObjectStates.waiting_message)


@mass_mailing_router.message(F.text, StateFilter(NotifyObjectStates.waiting_message), UserInfo())
async def process_mass_mailing_message(message: Message, state: FSMContext, user_info: User) -> None:
    """Обработчик для получения сообщения для массовой рассылки"""
    data = await state.get_data()

    object_id = data["object_id"]
    await message.delete()  
    await message.bot.delete_message(
        chat_id=message.chat.id,
        message_id=data.get('last_senden_msg_id'),
    )

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
        if not members:
            await message.answer(get_text("no_object_members", user_info.language))
            return
        
        for member in members:
            if member.telegram_id != user_info.telegram_id: 
                try:
                    await message.bot.send_message(
                        chat_id=member.telegram_id,
                        text=notification_text,
                    )
                except Exception as e:
                    logger.error(f"Ошибка при отправке сообщения рабочему {member.telegram_id}: {e}")
                    continue  

    await message.answer(
        text=get_text('notification_sent', user_info.language)
    )
    await state.clear()