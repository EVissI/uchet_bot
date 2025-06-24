from datetime import datetime, timedelta
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.bot.common.excel.utils import create_profic_report
from app.bot.common.texts import get_text, get_all_texts
from app.bot.filters.user_info import UserInfo
from app.bot.common.states import AdminPanelStates
from app.bot.kbds.inline_kbds import (
    get_finance_report_type_kbd,
    get_finance_period_kbd,
    get_finance_objects_kbd,
)
from app.bot.kbds.inline_kbds import (
    FinanceReportTypeCallback,
    FinanceReportPeriodCallback,
    FinanceReportObjectCallback,
)
from app.db.database import async_session_maker
from app.db.dao import ObjectProficAccountingDAO, ObjectCheckDAO, ObjectDAO, CheckDAO, ProficAccountingDAO
from app.db.models import User, Object
from app.db.schemas import ObjectFilterModel

from loguru import logger

finance_report_router = Router()


@finance_report_router.message(
    F.text.in_(get_all_texts("finance_report_btn")),
    UserInfo(),
)
async def start_finance_report(message: Message, user_info: User):
    """Handler for starting financial report generation"""
    await message.answer(
        text=get_text("select_report_type", user_info.language),
        reply_markup=get_finance_report_type_kbd(user_info.language),
    )


@finance_report_router.callback_query(
    FinanceReportTypeCallback.filter(),
    UserInfo(),
)
async def process_report_type(
    callback: CallbackQuery,
    callback_data: FinanceReportTypeCallback,
    state: FSMContext,
    user_info: User,
):
    """Process report type selection"""
    await callback.answer()

    if callback_data.action == "by_object":
        async with async_session_maker() as session:
            objects = await ObjectDAO.find_all(session, ObjectFilterModel())
            await callback.message.edit_text(
                text=get_text("select_object", user_info.language),
                reply_markup=get_finance_objects_kbd(objects, lang=user_info.language),
            )
            await state.update_data(report_type="by_object")

    if callback_data.action == "no_object":
        await callback.message.edit_text(
            text=get_text("select_period", user_info.language),
            reply_markup=get_finance_period_kbd(user_info.language),
        )
        await state.update_data(report_type="no_object")


@finance_report_router.callback_query(
    FinanceReportObjectCallback.filter(),
    UserInfo(),
)
async def process_object_selection(
    callback: CallbackQuery,
    callback_data: FinanceReportObjectCallback,
    state: FSMContext,
    user_info: User,
):
    """Process object selection and navigation"""
    await callback.answer()

    if callback_data.action in ["prev", "next"]:
        async with async_session_maker() as session:
            objects = await ObjectDAO.find_all(session, ObjectFilterModel())
            await callback.message.edit_reply_markup(
                reply_markup=get_finance_objects_kbd(
                    objects, page=callback_data.page, lang=user_info.language
                )
            )
    if callback_data.action == "select":
        await state.update_data(selected_object_id=callback_data.object_id)
        await callback.message.edit_text(
            text=get_text("select_period", user_info.language),
            reply_markup=get_finance_period_kbd(user_info.language),
        )
    if callback_data.action == "back":
        await callback.message.edit_text(
            text=get_text("select_report_type", user_info.language),
            reply_markup=get_finance_report_type_kbd(user_info.language),
        )
        await state.clear()
        return


@finance_report_router.callback_query(
    FinanceReportPeriodCallback.filter(),
    UserInfo(),
)
async def process_period_selection(
    callback: CallbackQuery,
    callback_data: FinanceReportPeriodCallback,
    state: FSMContext,
    user_info: User,
):
    """Process period selection"""
    await callback.answer()
    await callback.message.delete()
    if callback_data.action == "month":
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        await generate_report(callback.message, start_date, end_date, state, user_info)

    if callback_data.action == "all_time":
        end_date = datetime.now()
        start_date = datetime(2024, 1, 1)
        await generate_report(callback.message, start_date, end_date, state, user_info)

    if callback_data.action == "custom":
        await callback.message.answer(
            text=get_text("enter_period", user_info.language)
        )
        await state.set_state(AdminPanelStates.enter_period)
    if callback_data.action == "back":
        state_data = await state.get_data()
        if state_data.get("report_type") == "by_object":
            async with async_session_maker() as session:
                objects = await ObjectDAO.find_all(session, ObjectFilterModel())
                await callback.message.answer(
                    text=get_text("select_object", user_info.language),
                    reply_markup=get_finance_objects_kbd(
                        objects, lang=user_info.language
                    ),
                )
        else:
            await callback.message.answer(
                text=get_text("select_report_type", user_info.language),
                reply_markup=get_finance_report_type_kbd(user_info.language),
            )
        return


@finance_report_router.message(
    StateFilter(AdminPanelStates.enter_period),
    UserInfo(),
)
async def process_custom_period(message: Message, state: FSMContext, user_info: User):
    """Process custom period input"""
    try:
        dates = message.text.split("-")
        start_date = datetime.strptime(dates[0].strip(), "%d.%m.%Y")
        end_date = (
            datetime.strptime(dates[1].strip(), "%d.%m.%Y")
            if len(dates) > 1
            else datetime.now()
        )

        await generate_report(message, start_date, end_date, state, user_info)
        await state.clear()
    except:
        await message.answer(text=get_text("invalid_period_format", user_info.language))


async def generate_report(
    message: Message,
    start_date: datetime,
    end_date: datetime,
    state: FSMContext,
    user_info: User,
):
    """Generate and send financial report"""
    try:
        msg = await message.answer(text=get_text("generating_report", user_info.language))

        state_data = await state.get_data()
        report_type = state_data.get("report_type")
        object_id = (
            state_data.get("selected_object_id") if report_type == "by_object" else None
        )

        async with async_session_maker() as session:
            if report_type == "by_object":
                profic_records = await ObjectProficAccountingDAO.get_by_date_range(
                session, start_date=start_date, end_date=end_date, object_id=object_id
                )
                object_checks = await ObjectCheckDAO.get_by_date_range(
                    session,
                    start_date=start_date,
                    end_date=end_date,
                    object_id=object_id,
                )
                non_object_checks = None
            else:
                profic_records_obj = await ObjectProficAccountingDAO.get_by_date_range(
                    session, start_date=start_date, end_date=end_date
                )
                profic_records_general = await ProficAccountingDAO.get_by_date_range(
                    session, start_date=start_date, end_date=end_date
                )
                profic_records = list(profic_records_obj) + list(profic_records_general)

                object_checks = await ObjectCheckDAO.get_by_date_range(
                    session, start_date=start_date, end_date=end_date
                )
                non_object_checks = await CheckDAO.get_by_date_range(
                    session, start_date=start_date, end_date=end_date
                )

            excel_file = create_profic_report(
                profic_records=profic_records,
                object_checks=object_checks,
                non_object_checks=non_object_checks,
                start_date=start_date,
                end_date=end_date,
                lang=user_info.language,
            )

        await message.answer_document(
            document=BufferedInputFile(
                excel_file.read(),
                filename=f"financial_report_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.xlsx",
            ),
            caption=get_text("report_ready", user_info.language),
        )
        await msg.delete()
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        await message.answer(text=get_text("export_error", user_info.language))
    finally:
        await state.clear()
