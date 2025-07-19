import asyncio
from io import BytesIO
import re
from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message
from loguru import logger
from app.bot.common.states import AdminPanelStates, CreateCheckStatesWithUploadedPDF, PDFmanualInput
from app.bot.common.texts import get_text
from app.bot.common.utils import convert_pdf_to_jpg_bytes, extract_receipt_data
from app.bot.common.waiting_message import WaitingMessageManager
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import CheckOwnExpenseCallback, CheckTypeCallback, ObjListCallback, build_paginated_list_kbd, get_check_own_expense_kbd, get_check_type_select, get_manual_input_keyboard
from app.bot.kbds.markup_kbds import MainKeyboard
from app.db.models import User
from app.db.database import async_session_maker
from app.db.schemas import CheckModel, ObjectFilterModel, ObjectCheckModel,CheckFilterModel, ObjectCheckFilterModel
from app.db.dao import CheckDAO, ObjectCheckDAO, ObjectDAO

from app.config import settings


generate_file_id_router = Router()

@generate_file_id_router.message(F.document.mime_type == "application/pdf", StateFilter(None, AdminPanelStates), UserInfo())
async def handle_pdf(message: Message, bot: Bot, state: FSMContext, user_info: User):
    try:
        waiting_manager = WaitingMessageManager(message.chat.id, bot)
        await waiting_manager.start()
        file = await bot.get_file(message.document.file_id)
        file_bytes = await bot.download_file(file.file_path)
        loop = asyncio.get_running_loop()
        jpg_bytes, _ = await loop.run_in_executor(None, convert_pdf_to_jpg_bytes, file_bytes.read())
        data = await loop.run_in_executor(None, extract_receipt_data, jpg_bytes)
        description = "Чек сгенерирован автоматически из PDF"
        if message.caption:
            description = message.caption.strip()
        if not data.get("amount"):
            await waiting_manager.stop()
            
            photo = await message.answer_photo(
                photo=BufferedInputFile(jpg_bytes, filename="converted.jpg"),
                caption="Не смог определить формат чека. Давай заполним в ручную!",
                reply_markup=get_manual_input_keyboard()
            )
            await state.update_data(
                file_id=photo.photo[-1].file_id,
                amount=data.get("amount"),
                description=description,
            )
            return

        photo = await message.answer_photo(
            photo=BufferedInputFile(jpg_bytes, filename="converted.jpg"),
            caption=f"🧾 Дата транкзакции: {data.get('date')}\n💸 Сумма: {data.get('amount')} ₽\n🏦 Банк: {data.get('bank', 'Не определён')}",
            reply_markup=get_check_type_select()
        )
        await state.update_data(
            file_id=photo.photo[-1].file_id,
            date=data.get("date"),
            amount=data.get("amount"),
            description=description,
        )
        await waiting_manager.stop()
    except Exception as e:
        logger.error(f"Error processing PDF for user {message.from_user.id} - {e}")
        await message.reply("Ошибка конвертации пдф")


@generate_file_id_router.callback_query(F.data == "manual_input_start", UserInfo())
async def start_manual_input(callback: CallbackQuery, state: FSMContext, user_info: User):
    data = await state.get_data()
    if not data.get("file_id"):
        await callback.answer("Ошибка: нет данных для ручного ввода")
        return
    await callback.message.edit_caption(
        caption=None,
        reply_markup=None
    )
    await callback.message.answer(
        text=get_text("manual_input_prompt", user_info.language),
    )
    await state.set_state(PDFmanualInput.amount)
    await state.update_data(
        file_id=data.get("file_id"),
        amount=None,
        description=data.get("description")
    )


@generate_file_id_router.message(StateFilter(PDFmanualInput.amount), UserInfo())
async def process_manual_input(message: Message, state: FSMContext, user_info: User):
    try:
        text = message.text.strip()
        if not re.match(r'^\d+$', text):
            await message.reply(get_text("manual_input_error_amount", user_info.language))
            return

        await state.update_data(amount=text)
        await message.reply(
            f"{get_text('manual_input_success', user_info.language)}",
            reply_markup=get_check_type_select()
        )
        await state.clear()
    except Exception as e:
        logger.error(f"Error in manual input for user {message.from_user.id} - {e}")
        await message.reply(get_text("manual_input_error", user_info.language))


@generate_file_id_router.callback_query(CheckTypeCallback.filter(F.type == "object"), UserInfo())
async def handle_object_check_type(callback: CallbackQuery, callback_data: CheckTypeCallback, state: FSMContext, user_info: User):
    """Handle object check type selection"""
    await callback.answer()
    await callback.message.edit_reply_markup(reply_markup=None)
    async with async_session_maker() as session:
        objects = await ObjectDAO.find_all(session=session, filters=ObjectFilterModel(is_active=True))
        if not objects:
            await callback.message.answer(
                text=get_text('no_objects_found', user_info.language),
                reply_markup=MainKeyboard.build_main_kb(user_info.role, user_info.language)
            )
            return
        await state.update_data(
            type=callback_data.type,
        )
        await callback.message.answer(
            text=get_text('select_object', user_info.language),
            reply_markup=build_paginated_list_kbd(objects, context="generate_file_id_object")
        )


@generate_file_id_router.callback_query(ObjListCallback.filter((F.action == "select") & (F.context == "generate_file_id_object")), UserInfo())
async def handle_object_selection(callback: CallbackQuery, callback_data: ObjListCallback, state: FSMContext, user_info: User):
    """Handle object selection for check creation"""
    await callback.message.delete()
    async with async_session_maker() as session:
        selected_object = await ObjectDAO.find_one_or_none(session, filters=ObjectFilterModel(id=callback_data.id))
        if not selected_object:
            await callback.message.answer(get_text("object_not_found", user_info.language))
            return 
        
        await callback.message.answer(
            text=get_text("check_own_expense_required", user_info.language),
            reply_markup=get_check_own_expense_kbd(selected_object.id, user_info.language)
        )
        
        await state.update_data(object_id=selected_object.id, object_name=selected_object.name)

@generate_file_id_router.callback_query(CheckTypeCallback.filter(F.type == "general"), UserInfo())
async def handle_generate_check_type(callback: CallbackQuery, callback_data: CheckTypeCallback, state: FSMContext, user_info: User):
    """Handle general check type selection"""
    await callback.message.edit_reply_markup(reply_markup=None)
    last_message = await callback.message.answer(
        text=get_text("check_own_expense_required", user_info.language),
        reply_markup=get_check_own_expense_kbd(0, user_info.language)
    )
    await state.update_data(
        type=callback_data.type,
    )
    await state.update_data(last_message_id=last_message.message_id)


@generate_file_id_router.callback_query(CheckOwnExpenseCallback.filter(), UserInfo())
async def handle_object_check_type(callback: CallbackQuery, callback_data: CheckOwnExpenseCallback, state: FSMContext, user_info: User):
    """Handle object check type selection"""
    await callback.message.delete()
    data = await state.get_data()
    file_id = data.get("file_id")
    amount = data.get("amount")
    description = data.get("description")
    own_expense = callback_data.flag 
    type_ = data.get("type")
    if not file_id:
        await callback.message.answer(
            text=get_text("file_id_generation_error", user_info.language)
        )
        return
    if type_ == "general":
        async with async_session_maker() as session:
            await CheckDAO.add(
                session=session,
                values=CheckModel(
                    file_id=file_id,
                    amount=amount,
                    user_id=user_info.telegram_id,
                    description=description,
                    own_expense=own_expense,
                )   
            )  
        check_text = get_text(
            "out_object_check_format",
            "ru",
            worker_name=user_info.user_enter_fio,
            username=f"@{user_info.username}" if user_info.username else "нет username",
            description=description if description else "-",
            amount=amount,
        )
        await callback.bot.send_photo(
            chat_id=settings.TELEGRAM_GROUP_ID_CHEKS,
            photo=data["file_id"],
            caption=check_text,
        )

    if type_ == "object":
        object_id = data.get("object_id")
        if not object_id:
            await callback.message.reply(
                text=get_text("object_not_selected", user_info.language)
            )
            return
        async with async_session_maker() as session:
            await ObjectCheckDAO.add(
                session=session,
                values=ObjectCheckModel(
                    file_id=file_id,
                    amount=amount,
                    user_id=user_info.telegram_id,
                    description=description,
                    own_expense=own_expense,
                    object_id=object_id,
                )   
            )
        async with async_session_maker() as session:
            object = await ObjectDAO.find_one_or_none(session,filters=ObjectFilterModel(id = object_id))
        check_text = get_text(
            'check_format',
            user_info.language,
            object_name=object.name,
            worker_name=user_info.user_enter_fio,
            username=f"@{user_info.username}" if user_info.username else "нет username",
            description=description if description else "-",
            amount=amount
        )
        
        await callback.bot.send_photo(
            chat_id=settings.TELEGRAM_GROUP_ID_CHEKS,
            photo=data['file_id'],
            caption=check_text,
        )

    await callback.message.answer(
        text=get_text("check_created", user_info.language),
    )


@generate_file_id_router.message(F.photo,StateFilter(None, AdminPanelStates),UserInfo())
async def process_photo_for_file_id(message: Message, user_info: User):
    """Generate and return file_id from photo"""
    try:
        file_id = message.photo[-1].file_id
        logger.info(f"Generated file_id for user {user_info.telegram_id}: {file_id}")
        
        await message.reply(
            text=get_text(
                "file_id_generated",
                user_info.language,
                file_id=f"`{file_id}`"
            ),
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Error generating file_id for user {user_info.telegram_id}: {e}")
        await message.reply(
            text=get_text("file_id_generation_error", user_info.language)
        )

@generate_file_id_router.message(F.text.regexp(r"^[A-Za-z0-9_-]{20,}$"), StateFilter(None, AdminPanelStates), UserInfo())
async def process_file_id_as_text(message: Message, user_info: User):
    """Отправить фото по file_id, если пользователь прислал file_id текстом"""
    file_id = message.text.strip()
    try:
        try:
            await message.reply_photo(
                photo=file_id,
                parse_mode="Markdown"
            )
        except:
            await message.reply_document(
                document=file_id,
                parse_mode="Markdown"
            )
    except Exception as e:
        logger.error(f"Error sending photo by file_id for user {user_info.telegram_id}: {e}")
        await message.reply(
            text=get_text("file_id_generation_error", user_info.language)
        )