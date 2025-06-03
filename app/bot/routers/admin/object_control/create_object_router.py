from aiogram import Router,F
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from loguru import logger

from app.bot.common.texts import get_text, get_all_texts
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import ObjectDocumentTypeCallback, UploadWithoutDocumentsCallback, get_obj_document_type_kbd, get_updload_without_documents_kbd
from app.bot.kbds.markup_kbds import AdminObjectControlKeyboard, get_dialog_keyboard, stop_kb
from app.bot.common.states import CreateObjectStates,AdminPanelStates
from app.bot.common.fsm_managment import StateHistoryMixin, DialogMessageManager
from app.db.database import async_session_maker
from app.db.dao import ObjectDAO, ObjectDocumentDAO
from app.db.schemas import ObjectDocumentModel, ObjectModel
from app.config import bot

from app.db.models import User

class CreateObjectRouter(Router, StateHistoryMixin, DialogMessageManager):
    def __init__(self):
        super().__init__()

create_object_router = CreateObjectRouter()


@create_object_router.message(F.text.in_(get_all_texts('create_object_btn')), StateFilter(AdminPanelStates.objects_control),UserInfo())
async def process_create_object(message:Message,state:FSMContext, user_info:User):
    await create_object_router.save_state_history(state, CreateObjectStates.waiting_name.state)
    await create_object_router.save_message(state, message.message_id)
    bot_message =await message.answer(
        text=get_text('create_object_name', user_info.language),
        reply_markup=get_dialog_keyboard(user_info.language)
    )
    await state.set_state(CreateObjectStates.waiting_name.state)
    await create_object_router.save_message(state, bot_message.message_id)


@create_object_router.message(F.text.in_(get_all_texts('cancel_btn')), UserInfo(), StateFilter(CreateObjectStates))
async def process_cancel_button(message: Message, state: FSMContext, user_info: User):
    await create_object_router.save_message(state, message.message_id)
    await state.set_state(AdminPanelStates.objects_control.state)
    await create_object_router.clear_messages(state, message.chat.id, bot)
    await message.answer(
        text=get_text('operation_cancelled', user_info.language),
        reply_markup=AdminObjectControlKeyboard.build_object_control_kb(user_info.language)
    )


@create_object_router.message(F.text.in_(get_all_texts('back_btn')), UserInfo(), StateFilter(CreateObjectStates))
async def process_back_button(message: Message, state: FSMContext, user_info: User):
    await create_object_router.save_message(state, message.message_id)
    previous_state = await create_object_router.get_previous_state(state)

    await state.set_state(previous_state)
    match previous_state:
        case AdminPanelStates.objects_control.state:
            await state.set_state(AdminPanelStates.objects_control.state)
            await create_object_router.clear_messages(state, message.chat.id, bot)
            await message.answer(
                text=get_text('operation_cancelled', user_info.language),
                reply_markup=AdminObjectControlKeyboard.build_object_control_kb(user_info.language)
            )
            return
        case CreateObjectStates.waiting_name.state:
            bot_message = await message.answer(
                text=get_text('create_object_name', user_info.language),
                reply_markup=get_dialog_keyboard(user_info.language)
            )

        case CreateObjectStates.waiting_description.state:
            bot_message = await message.answer(
                text=get_text('create_object_description', user_info.language),
                reply_markup=get_dialog_keyboard(user_info.language)
            )
    await create_object_router.save_message(state, bot_message.message_id)


@create_object_router.message(F.text, StateFilter(CreateObjectStates.waiting_name), UserInfo())
async def process_object_name(message: Message, state: FSMContext, user_info: User):
    await create_object_router.save_message(state, message.message_id)
    await state.update_data(name=message.text)
    await create_object_router.save_state_history(state, CreateObjectStates.waiting_description.state)
    
    bot_message = await message.answer(
        text=get_text('create_object_description', user_info.language),
        reply_markup=get_dialog_keyboard(user_info.language)
    )      
    await create_object_router.save_message(state, bot_message.message_id)      


@create_object_router.message(F.text, StateFilter(CreateObjectStates.waiting_description), UserInfo())
async def process_object_description(message: Message, state: FSMContext, user_info: User):
    await create_object_router.save_message(state, message.message_id)
    await create_object_router.save_state_history(state, CreateObjectStates.waiting_documents.state)
    await state.update_data(description=message.text)
    await state.set_state(CreateObjectStates.waiting_documents.state)
    bot_message = await message.answer(
        text=get_text('create_object_documents', user_info.language,reply_markup=stop_kb(user_info.language)),
        reply_markup=get_dialog_keyboard(user_info.language)
    )
    await create_object_router.save_message(state, bot_message.message_id)

@create_object_router.message(F.photo, StateFilter(CreateObjectStates.waiting_documents), UserInfo())
async def process_object_documents(message: Message, state: FSMContext, user_info: User):
    await create_object_router.save_message(state, message.message_id)
    data = await state.get_data()
    saved_documents = data.get('saved_documents', [])
    saved_documents.append(message.photo[-1].file_id)
    await state.update_data(saved_documents=saved_documents)
    
    bot_message = await message.answer(
        text=get_text('create_object_document_has_received', user_info.language),
        reply_markup=get_dialog_keyboard(user_info.language)
    )
    await create_object_router.save_message(state, bot_message.message_id)

@create_object_router.message(~F.photo, StateFilter(CreateObjectStates.waiting_documents), UserInfo())
async def unprocess_object_documents(message: Message, state: FSMContext, user_info: User):
    await create_object_router.save_message(state, message.message_id)
    bot_message = await message.answer(
        text=get_text('create_object_document_no_received', user_info.language),
        reply_markup=stop_kb(user_info.language)
    )
    await create_object_router.save_message(state, bot_message.message_id)

@create_object_router.message(F.text.in_(get_all_texts('stop_upload_btn')), UserInfo(), StateFilter(CreateObjectStates))
async def finish_document_received(message: Message, state: FSMContext, user_info: User):
    await create_object_router.save_message(state, message.message_id)
    data = await state.get_data()
    saved_documents = data.get('saved_documents', [])

    if not saved_documents:
        bot_message = await message.answer(
            text=get_text('create_object_no_documents', user_info.language),
            reply_markup=get_updload_without_documents_kbd(user_info.language)
        )
        await create_object_router.save_message(state, bot_message.message_id)
        return
    
    

async def send_next_document(message: Message, state: FSMContext, user_info: User):
    """Helper function to send next document for type selection"""
    data = await state.get_data()
    saved_documents = data.get('saved_documents', [])
    current_index = data.get('current_doc_index', 0)
    
    if current_index < len(saved_documents):
        bot_message = await message.answer_photo(
            photo=saved_documents[current_index],
            caption=get_text('select_document_type', user_info.language),
            reply_markup=get_obj_document_type_kbd(user_info.language, current_index)
        )
        await create_object_router.save_message(state, bot_message.message_id)
    else:
        await create_object_with_documents(message, state, user_info)

async def create_object_with_documents(message: Message, state: FSMContext, user_info: User):
    """Create object with all processed documents"""
    data = await state.get_data()
    
    async with async_session_maker() as session:
        object_model = ObjectModel(
            name=data['name'],
            description=data['description'],
            is_active=True,
            creator_id=user_info.telegram_id,
        )
        
        await ObjectDAO.add(session, object_model)
        new_object = await ObjectDAO.find_one_or_none(session, filters=object_model)
        documents = []
        for doc in data['document_types']:
            documents.append(ObjectDocumentModel(
                file_id=doc['file_id'],
                document_type=doc['type'],
                object_id=new_object.id
            ))
        await ObjectDocumentDAO.add_many(session, documents)
        
        await create_object_router.clear_messages(state, message.chat.id, bot)
        await state.set_state(AdminPanelStates.objects_control)
        await message.answer(
            text=get_text('create_object_success', user_info.language),
            reply_markup=AdminObjectControlKeyboard.build_object_control_kb(user_info.language)
        )


@create_object_router.callback_query(ObjectDocumentTypeCallback.filter(), StateFilter(CreateObjectStates))
async def process_document_type(
    callback: CallbackQuery, 
    callback_data: ObjectDocumentTypeCallback, 
    state: FSMContext, 
    user_info: User
):
    """Handle document type selection"""
    data = await state.get_data()
    saved_documents = data.get('saved_documents', [])
    document_types = data.get('document_types', [])
    
    document_types.append({
        'file_id': saved_documents[callback_data.document_index],
        'type': callback_data.type
    })
    
    await state.update_data(
        document_types=document_types,
        current_doc_index=callback_data.document_index + 1
    )
    
    await callback.message.delete()
    
    await send_next_document(callback.message, state, user_info)

@create_object_router.callback_query(UploadWithoutDocumentsCallback.filter(), UserInfo(), StateFilter(CreateObjectStates))
async def process_upload_without_documents(callback: CallbackQuery, callback_data: UploadWithoutDocumentsCallback, state: FSMContext, user_info: User):
    data = await state.get_data()
    async with async_session_maker() as session:    
        object_model = ObjectModel(
            name=data['name'],
            description=data['description'],
            is_active=True,
            creator_id=user_info.telegram_id,
        )
        
        await ObjectDAO.add(session, object_model)       
        await create_object_router.clear_messages(state, callback.message.chat.id, bot)
        await state.set_state(AdminPanelStates.objects_control)
        await callback.message.answer(
            text=get_text('create_object_success', user_info.language),
            reply_markup=AdminObjectControlKeyboard.build_object_control_kb(user_info.language)
        )