from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.bot.common.states import ObjectCheckStates
from app.bot.common.texts import get_text
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import ForemanObjectCallback, ForemanOwnExpenseCallback, get_back_kbd, get_own_expense_kbd
from app.db.dao import ObjectCheckDAO
from app.db.models import User
from app.db.database import async_session_maker
from app.db.schemas import ObjectCheckModel
from app.config import settings

receipts_router = Router()


@receipts_router.callback_query(ForemanObjectCallback.filter(F.action == "receipts"), UserInfo())
async def process_check_btn(
    callback: CallbackQuery,
    callback_data: ForemanObjectCallback,
    state: FSMContext,
    user_info: User
) -> None:
    """Handler for check button"""
    await state.update_data(object_id=callback_data.object_id)
    await state.set_state(ObjectCheckStates.waiting_photo_and_desription)
    
    last_message = await callback.message.answer(
        text=get_text('send_check_photo_and_description', user_info.language,
                      reply_markup=get_back_kbd(user_info.language, callback_data.object_id))
    )
    await state.update_data(last_senden_msg_id=last_message.message_id)
    await callback.message.delete()
    await callback.answer()


@receipts_router.message(F.photo, StateFilter(ObjectCheckStates.waiting_photo_and_desription), UserInfo())
async def process_check_description(
    message: Message, 
    state: FSMContext, 
    user_info: User
) -> None:
    """Handler for receiving check photo and description"""
    data = await state.get_data()
    await message.delete()
    await message.bot.delete_message(
        chat_id=message.chat.id,
        message_id=data.get('last_senden_msg_id'),
    )

    await state.update_data(photo_id=message.photo[-1].file_id)
    await state.update_data(description=message.text)
    await state.update_data(own_expense=False)
    await state.set_state(ObjectCheckStates.waiting_amount)
    
    last_message = await message.answer(
        text=get_text('enter_check_amount', user_info.language),
        reply_markup=get_own_expense_kbd(user_info.language, flag=False)
    )
    await state.update_data(last_senden_msg_id=last_message.message_id)


@receipts_router.message(StateFilter(ObjectCheckStates.waiting_amount), UserInfo())
async def process_check_amount(
    message: Message, 
    state: FSMContext, 
    user_info: User
) -> None:
    """Handler for receiving check amount"""
    await message.delete()
    await message.bot.delete_message(
        chat_id=message.chat.id,
        message_id=state.get_data().get('last_senden_msg_id'),
    )
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
                own_expense=data['own_expense'],
                object_id=data['object_id'],
                user_id=user_info.telegram_id,
            )
        )

    await message.answer(
        text=get_text('check_saved', user_info.language)
    )
    await state.clear()


@receipts_router.message(~F.photo, StateFilter(ObjectCheckStates.waiting_photo_and_desription), UserInfo())
async def process_invalid_check_photo(message: Message, user_info: User) -> None:
    """Handler for invalid input in check photo state"""
    await message.answer(
        text=get_text('send_photo_only', user_info.language)
    )

@receipts_router.callback_query(ForemanOwnExpenseCallback.filter())
async def process_own_expense_btn(
    callback: CallbackQuery,
    callback_data: ForemanOwnExpenseCallback,
    state: FSMContext,
    user_info: User
) -> None:
    """Handler for own expense button"""
    await state.update_data(own_expense=not callback_data.flag)
    await callback.message.edit_reply_markup(
        reply_markup=get_own_expense_kbd(user_info.language, flag=not callback_data.flag)
    )