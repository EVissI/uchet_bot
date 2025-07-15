from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from datetime import datetime

from loguru import logger

from app.bot.common.excel.google_excel import append_object_material_order_to_sheet
from app.bot.common.states import MaterialOrderStates
from app.bot.common.texts import get_all_texts, get_text
from app.bot.filters.role_filter import RoleFilter
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import MaterialOrderTypeCallback, ObjListCallback, build_paginated_list_kbd, get_material_order_type_select
from app.bot.kbds.markup_kbds import get_back_keyboard,MainKeyboard
from app.db.dao import MaterialOrderDAO, ObjectDAO, ObjectMaterialOrderDAO
from app.db.models import User
from app.db.database import async_session_maker
from app.db.schemas import MaterialOrderModel, MaterialOrderFilter, ObjectFilterModel, ObjectMaterialOrderModel, ObjectMaterialOrderFilter
from app.config import settings

material_order_router = Router()

@material_order_router.message(
    F.text.in_(get_all_texts("material_order_btn")), UserInfo()
)
async def process_material_order(message: Message, state: FSMContext, user_info: User):
    await message.answer(
        text=get_text("select_material_order_type", user_info.language),
        reply_markup=get_material_order_type_select(context='create', 
                                                    lang=user_info.language)
    )


@material_order_router.callback_query(MaterialOrderTypeCallback.filter((F.type=="object") & (F.context=='create')), UserInfo())
async def process_material_order_object_type_select(callback: CallbackQuery, state: FSMContext, user_info: User):
    async with async_session_maker() as session:
        objects = await ObjectDAO.find_all(session, filters=ObjectFilterModel(is_active=True))
        if not objects:
            await callback.message.answer(
                text=get_text('no_objects_found', user_info.language),
                reply_markup=MainKeyboard.build_main_kb(user_info.role, user_info.language)
            )
            return
        await callback.message.delete()
        if user_info.role in [User.Role.admin.value, User.Role.buyer.value]:
            await callback.message.answer(get_text("select_object",user_info.language),
                                            reply_markup=build_paginated_list_kbd(objects,
                                                                                context='material_order_object', object_type = 'all_objects'))
        else:
            await callback.message.answer(get_text("select_object",user_info.language),
                                            reply_markup=build_paginated_list_kbd(objects,
                                                                                context='material_order_object', object_type = 'object'))


@material_order_router.callback_query(ObjListCallback.filter((F.action == "select") & (F.context == "material_order_object")), UserInfo())
async def process_material_order_object_select(callback: CallbackQuery, callback_data: ObjListCallback, state: FSMContext, user_info: User):
    async with async_session_maker() as session:
        selected_object = await ObjectDAO.find_one_or_none(session, filters=ObjectFilterModel(id=callback_data.id))
        if not selected_object:
            await callback.message.answer(get_text("object_not_found", user_info.language))
            return 
        await callback.message.delete() 
        await callback.message.answer(
            text=get_text("enter_material_order", user_info.language),
            reply_markup=get_back_keyboard(user_info.language)
        )
        await state.update_data(object_id=callback_data.id, 
                                order_type="object",
                                object_name=selected_object.name)
        await state.set_state(MaterialOrderStates.waiting_description)


@material_order_router.callback_query(MaterialOrderTypeCallback.filter((F.type=="general") & (F.context=='create')), UserInfo())
async def process_material_order_general_type_select(callback: CallbackQuery, state: FSMContext, user_info: User):
    await callback.message.delete()
    await callback.message.answer(
        text=get_text("enter_material_order", user_info.language),
        reply_markup=get_back_keyboard(user_info.language)
    )
    await state.set_state(MaterialOrderStates.waiting_description)
    await state.update_data(order_type="general")


@material_order_router.message(F.text.in_(get_all_texts("back_btn")),
                            StateFilter(MaterialOrderStates),
                            UserInfo())
async def cmd_back(message: Message, state: FSMContext, user_info: User):
    """Handler for back button in material order process"""
    await state.clear()
    await message.answer(
        text=get_text(message.text, user_info.language),
        reply_markup=MainKeyboard.build_main_kb(user_info.role, user_info.language)
    )

@material_order_router.message(
    F.text,
    StateFilter(MaterialOrderStates.waiting_description), 
    UserInfo()
)
async def process_order_description(
    message: Message, state: FSMContext, user_info: User
):
    """Handler for receiving material description"""
    await state.update_data(description=message.text)
    await state.set_state(MaterialOrderStates.waiting_date)
    await message.answer(text=get_text("enter_delivery_date", user_info.language))


@material_order_router.message(
    StateFilter(MaterialOrderStates.waiting_date),
    F.text.regexp(r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(20\d{2})$"),
    UserInfo(),
)
async def process_valid_date(message: Message, state: FSMContext, user_info: User):
    """Handler for processing valid date format"""
    try:
        try:
            day, month, year = map(int, message.text.split("."))
            input_date = datetime(year, month, day)
            today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            if input_date < today:
                await message.answer(
                    text=get_text("date_must_be_future", user_info.language)
                )
                return
        except ValueError:
            await message.answer(text=get_text("invalid_date", user_info.language))
            return

        data = await state.get_data()

        if data.get("order_type") == "general":
            order_text = get_text(
                "material_order_format",
                lang = "ru",
                worker_name=user_info.user_enter_fio,
                username=f"@{user_info.username}" if user_info.username else "нет username",
                description=data["description"],
                delivery_date=message.text,
            )
            sent_message = await message.bot.send_message(
                chat_id=settings.TELEGRAM_GROUP_ID_MATERIAL_ORDER,
                text=order_text,
            )
            async with async_session_maker() as session:
                await MaterialOrderDAO.add(
                    session,
                    MaterialOrderModel(
                        description=data["description"],
                        delivery_date=message.text,
                        message_id=sent_message.message_id,
                    ),
                )
            await message.answer(text=get_text("order_saved", user_info.language))
            async with async_session_maker() as session:
                order = await MaterialOrderDAO.find_one_or_none(
                    session=session,
                    filters=MaterialOrderFilter(message_id=sent_message.message_id)
                )
                append_object_material_order_to_sheet(
                    order,
                    sent_message=sent_message,
                    spreadsheet_id='11txWijAXs5_s8BkP1bxusyh5LW0EA93sVhYv93YWI_w',
                    worksheet_name='Ответы на форму (1)'
                )
        if data.get("order_type") == "object":
            order_text = get_text(
                "material_order_format_object",
                lang = "ru",
                worker_name=user_info.user_enter_fio,
                username=f"@{user_info.username}" if user_info.username else "нет username",
                description=data["description"],
                delivery_date=message.text,
                object_id=data["object_id"],
                object_name=data.get("object_name", "Не указано"),
            )
            sent_message = await message.bot.send_message(
                chat_id=settings.TELEGRAM_GROUP_ID_MATERIAL_ORDER,
                text=order_text,
                reply_markup=get_back_keyboard(user_info.language)
            )
            async with async_session_maker() as session:
                await ObjectMaterialOrderDAO.add(
                    session,
                    ObjectMaterialOrderModel(
                        description=data["description"],
                        delivery_date=message.text,
                        object_id=data["object_id"],
                        message_id=sent_message.message_id,
                    ),
                )
            await message.answer(text=get_text("order_saved", user_info.language), 
                                reply_markup=MainKeyboard.build_main_kb(user_info.role, user_info.language))
            async with async_session_maker() as session:
                order = await ObjectMaterialOrderDAO.find_one_with_object(
                    session,
                    message_id=sent_message.message_id,
                )
                append_object_material_order_to_sheet(
                    order,
                    sent_message=sent_message,
                    spreadsheet_id='11txWijAXs5_s8BkP1bxusyh5LW0EA93sVhYv93YWI_w',
                    worksheet_name='Ответы на форму (1)'
                )
    except Exception as e:
        await message.answer(text=get_text("error_processing_order", user_info.language))
        logger.error(f"Error processing material order for user {user_info.telegram_id}: {e}")
    finally:  
        await state.clear()


@material_order_router.message(
    StateFilter(MaterialOrderStates.waiting_date),
    ~F.text.regexp(r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(20\d{2})$"),
    UserInfo(),
)
async def process_invalid_date_format(message: Message, user_info: User):
    """Handler for invalid date format"""
    await message.answer(text=get_text("invalid_date_format", user_info.language))
