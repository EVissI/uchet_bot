from loguru import logger

from aiogram import Router,F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from app.bot.common.states import ObjectPhotoStates
from app.bot.common.texts import get_text
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import ForemanObjectCallback
from app.db.dao import ObjectPhotoDAO
from app.db.models import User
from app.db.database import async_session_maker
from app.config import settings
from app.db.schemas import ObjectPhotoModel


object_photo_router = Router()

@object_photo_router.callback_query(ForemanObjectCallback.filter(F.action == 'photo'), UserInfo())
async def process_photo_btn(
    callback: CallbackQuery, 
    callback_data: ForemanObjectCallback, 
    state: FSMContext,
    user_info: User
):
    """Handler for photo button"""
    await callback.message.delete()
    await state.update_data(object_id=callback_data.object_id)
    await state.set_state(ObjectPhotoStates.waiting_photo)
    
    await callback.message.answer(
        text=get_text('send_object_photo', user_info.language)
    )

@object_photo_router.message(F.photo, StateFilter(ObjectPhotoStates.waiting_photo), UserInfo())
async def process_object_photo(message: Message, state: FSMContext, user_info: User):
    """Handler for receiving photo"""
    await state.update_data(photo_id=message.photo[-1].file_id)
    await state.set_state(ObjectPhotoStates.waiting_description)
    
    await message.answer(
        text=get_text('enter_photo_description', user_info.language)
    )


@object_photo_router.message(StateFilter(ObjectPhotoStates.waiting_description), UserInfo())
async def process_photo_description(message: Message, state: FSMContext, user_info: User):
    """Handler for receiving photo description"""
    data = await state.get_data()
    
    photo_text = get_text(
        'object_photo_format',
        user_info.language,
        object_id=data['object_id'],
        worker_name=user_info.user_enter_fio,
        username=f"@{user_info.username}" if user_info.username else "нет username",
        description=message.text
    )
    
    await message.bot.send_photo(
        chat_id=settings.TELEGRAM_GROUP_ID_OBJECT_PHOTO,
        photo=data['photo_id'],
        caption=photo_text,
    )
    async with async_session_maker() as session:
        await ObjectPhotoDAO.add(
            session,
            ObjectPhotoModel(
                file_id=data['photo_id'],
                description=message.text,
                object_id=data['object_id'],
                user_id=user_info.telegram_id,
            )
        )
    await message.answer(
        text=get_text('photo_sent', user_info.language)
    )
    await state.clear()