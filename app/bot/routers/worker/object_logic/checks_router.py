from aiogram import Router,F
from aiogram.types import CallbackQuery,Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.bot.common.states import ObjectCheckStates
from app.bot.common.texts import get_text
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import WorkerObjectActionCallback
from app.db.dao import ObjectCheckDAO
from app.db.models import User
from app.db.database import async_session_maker
from app.config import settings
from app.db.schemas import ObjectCheckModel


checks_router = Router()

@checks_router.callback_query(WorkerObjectActionCallback.filter(F.action == 'checks'), UserInfo())
async def process_check_btn(
    callback: CallbackQuery,
    callback_data: WorkerObjectActionCallback,
    state: FSMContext,
    user_info: User
):
    """Handler for check button"""
    await callback.message.delete()
    await state.update_data(object_id=callback_data.object_id)
    await state.set_state(ObjectCheckStates.waiting_photo_and_desription)
    
    await callback.message.answer(
        text=get_text('send_check_photo_and_description', user_info.language)
    )
    


@checks_router.message(F.photo,StateFilter(ObjectCheckStates.waiting_photo_and_desription), UserInfo())
async def process_check_description(message: Message, state: FSMContext, user_info: User):
    """Handler for receiving check description"""
    await state.update_data(photo_id=message.photo[-1].file_id)
    await state.update_data(description=message.caption)
    await state.set_state(ObjectCheckStates.waiting_amount)
    
    await message.answer(
        text=get_text('enter_check_amount', user_info.language)
    )

@checks_router.message(StateFilter(ObjectCheckStates.waiting_amount), UserInfo())
async def process_check_amount(message: Message, state: FSMContext, user_info: User):
    """Handler for receiving check amount"""
    try:
        amount = float(message.text.replace(',', '.'))
    except ValueError:
        await message.answer(
            text=get_text('invalid_amount', user_info.language)
        )
        return

    data = await state.get_data()
    
    check_text = get_text(
        'check_format',
        user_info.language,
        object_id=data['object_id'],
        worker_name=user_info.user_enter_fio,
        username=f"@{user_info.username}" if user_info.username else "нет username",
        description=data['description'],
        amount=amount
    )
    
    await message.bot.send_photo(
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
    
    await message.answer(
        text=get_text('check_saved', user_info.language)
    )
    await state.clear()

@checks_router.message(~F.photo, StateFilter(ObjectCheckStates.waiting_photo_and_desription), UserInfo())
async def process_invalid_check_photo(message: Message, user_info: User):
    """Handler for invalid input in check photo state"""
    await message.answer(
        text=get_text('send_photo_only', user_info.language)
    )