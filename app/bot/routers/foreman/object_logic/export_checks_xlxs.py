from datetime import datetime
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.bot.common.excel.utils import create_expense_report
from app.bot.common.states import ExportXlsxStates
from app.bot.common.texts import get_text
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import (
    ForemanObjectCallback, 
    get_back_kbd,
    get_expense_type_kbd,
    ForemanExpenseTypeCallback
)
from app.db.dao import ObjectCheckDAO
from app.db.models import User
from app.db.database import async_session_maker

export_router = Router()



@export_router.callback_query(ForemanObjectCallback.filter(F.action == "export_xlsx"), UserInfo())
async def process_export_btn(
    callback: CallbackQuery,
    callback_data: ForemanObjectCallback,
    state: FSMContext,
    user_info: User
) -> None:
    """Initial handler for export button"""
    await state.update_data(object_id=callback_data.object_id)
    await state.set_state(ExportXlsxStates.waiting_start_date)
    await callback.message.delete()
    
    last_message = await callback.message.answer(
        text=get_text("enter_start_date", user_info.language),
        reply_markup=get_back_kbd(user_info.language, callback_data.object_id)
    )
    await state.update_data(last_message_id=last_message.message_id)


@export_router.message(F.text.regexp(r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(20\d{2})$"),
                       StateFilter(ExportXlsxStates.waiting_start_date), 
                       UserInfo())
async def process_start_date(message: Message, state: FSMContext, user_info: User) -> None:
    """Handler for start date input"""
    try:
        start_date = datetime.strptime(message.text, "%d.%m.%Y")
        await state.update_data(start_date=start_date)
        await state.set_state(ExportXlsxStates.waiting_end_date)
        
        data = await state.get_data()
        await message.delete()
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=data['last_message_id']
        )
        
        last_message = await message.answer(
            text=get_text("enter_end_date", user_info.language),
            reply_markup=get_back_kbd(user_info.language, data['object_id'])
        )
        await state.update_data(last_message_id=last_message.message_id)
        
    except ValueError:
        await message.answer(text=get_text("invalid_date_format", user_info.language))


@export_router.message(F.text.regexp(r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(20\d{2})$"),
                        StateFilter(ExportXlsxStates.waiting_end_date),
                        UserInfo())
async def process_end_date(message: Message, state: FSMContext, user_info: User) -> None:
    """Handler for end date input"""
    try:
        end_date = datetime.strptime(message.text, "%d.%m.%Y")
        await state.update_data(end_date=end_date)
        await state.set_state(ExportXlsxStates.waiting_expense_type)
        
        data = await state.get_data()
        await message.delete()
        await message.bot.delete_message(
            chat_id=message.chat.id,
            message_id=data['last_message_id']
        )
        
        last_message = await message.answer(
            text=get_text("select_expense_type", user_info.language),
            reply_markup=get_expense_type_kbd(user_info.language, data['object_id'])
        )
        await state.update_data(last_message_id=last_message.message_id)
        
    except ValueError:
        await message.answer(text=get_text("invalid_date_format", user_info.language))


@export_router.callback_query(ForemanExpenseTypeCallback.filter(), UserInfo())
async def process_expense_type(
    callback: CallbackQuery,
    callback_data: ForemanExpenseTypeCallback,
    state: FSMContext,
    user_info: User
) -> None:
    """Handler for expense type selection"""
    data = await state.get_data()
    
    async with async_session_maker() as session:
        expenses = await ObjectCheckDAO.get_filtered_expenses(
            session,
            object_id=data['object_id'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            expense_type=callback_data.expense_type
        )
        
        if not expenses:
            await callback.message.edit_text(
                text=get_text("no_expenses_found", user_info.language)
            )
            await state.clear()
            return

        excel_file = create_expense_report(expenses, user_info.language)
        
        input_file = BufferedInputFile(
            excel_file.getvalue(),
            filename=f"expense_report_{data['start_date'].strftime('%d_%m_%Y')}-{data['end_date'].strftime('%d_%m_%Y')}.xlsx"
        )
        await callback.message.delete()
        await callback.message.answer_document(
            document=input_file,
            caption=get_text(
                "expense_report_caption",
                user_info.language,
                start_date=data['start_date'].strftime("%d.%m.%Y"),
                end_date=data['end_date'].strftime("%d.%m.%Y"),
                expense_type=callback_data.expense_type
            )
        )
    
    await state.clear()


@export_router.message(
    StateFilter(ExportXlsxStates.waiting_start_date or ExportXlsxStates.waiting_end_date),
    ~F.text.regexp(r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(20\d{2})$"),
    UserInfo()
)
async def process_invalid_start_date(message: Message, user_info: User) -> None:
    """Handler for invalid start date format"""
    await message.answer(text=get_text("invalid_date_format", user_info.language))