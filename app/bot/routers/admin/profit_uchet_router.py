﻿from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from loguru import logger

from app.bot.common.states import ProficAccountingStates, AdminPanelStates
from app.bot.common.texts import get_text,get_all_texts
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import AccountingTypeCallback, ObjListCallback, build_accounting_type_kb, build_paginated_list_kbd
from app.db.dao import ObjectDAO, ProficAccountingDAO
from app.db.models import User
from app.db.schemas import ProficAccountingModel
from app.db.database import async_session_maker

profic_router = Router()


@profic_router.message(
    F.text.in_(get_all_texts("profic_accounting_btn")),
    StateFilter(AdminPanelStates.main),
    UserInfo(),
)
async def start_profic_accounting(message: Message, state: FSMContext, user_info: User):
    """Start profit accounting process"""
    async with async_session_maker() as session:
        objects = await ObjectDAO.find_all(session)

        if not objects:
            await message.answer(get_text("no_objects_found", user_info.language))
            return

        await message.answer(
            text=get_text("select_object_for_profic", user_info.language),
            reply_markup=build_paginated_list_kbd(items=objects, context='admin_profic_accounting'),
        )


@profic_router.callback_query(ObjListCallback.filter((F.action == 'select') & (F.context== 'admin_profic_accounting')))
async def process_object_selection(
    callback: CallbackQuery, callback_data:ObjListCallback, state: FSMContext, user_info: User
):
    await callback.message.answer(
        text=get_text("select_accounting_type", user_info.language),
        reply_markup=build_accounting_type_kb(user_info.language),
    )
    await state.update_data(object_id=int(callback_data.id))


@profic_router.callback_query(AccountingTypeCallback.filter(),UserInfo())
async def process_accouting_type(
    callback: CallbackQuery, callback_data:AccountingTypeCallback, state: FSMContext, user_info: User
):
    await callback.message.answer(
        text=get_text("input_accounting_amount", user_info.language),
    )
    await state.update_data(type=callback_data.type)
    await state.set_state(ProficAccountingStates.enter_amount)


@profic_router.message(F.text, StateFilter(ProficAccountingStates.enter_amount))
async def process_amount(message: Message, state: FSMContext, user_info: User):
    """Handle amount input"""
    try:
        amount = float(message.text.replace(",", "."))
        if amount <= 0:
            raise ValueError("Amount must be positive")

        await state.update_data(amount=amount)
        await message.answer(text=get_text("enter_payment_purpose", user_info.language))
        await state.set_state(ProficAccountingStates.enter_purpose)

    except ValueError:
        await message.answer(get_text("invalid_amount", user_info.language))


@profic_router.message(StateFilter(ProficAccountingStates.enter_purpose))
async def process_purpose(message: Message, state: FSMContext, user_info: User):
    """Handle purpose input and save record"""
    data = await state.get_data()

    try:
        async with async_session_maker() as session:
            profic_data = ProficAccountingModel(
                object_id=data["object_id"],
                amount=data["amount"],
                purpose=message.text,
                payment_type=data["type"],
                created_by=user_info.telegram_id,
            )

            await ProficAccountingDAO.add(session, profic_data)

            await message.answer(
                text=get_text(
                    "profic_saved",
                    user_info.language,
                    amount=data["amount"],
                    type=data["payment_type"],
                )
            )
            await state.set_state(AdminPanelStates.main)

    except Exception as e:
        logger.error(f"Error saving profic record: {e}")
        await message.answer(get_text("profic_save_error", user_info.language))
