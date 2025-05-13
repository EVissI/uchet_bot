from aiogram import Router, F
from aiogram.types import Message,CallbackQuery
from aiogram.filters import Command,StateFilter
from aiogram.fsm.context import FSMContext

from app.bot.common.states import NotifyObjectStates, ObjectCheckStates, ObjectPhotoStates
from app.bot.common.texts import get_all_texts, get_text
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import ObjectActionCallback, object_keyboard
from app.db.dao import ObjectCheckDAO, ObjectDocumentDAO, ObjectMemberDAO, ObjectPhotoDAO
from app.db.database import async_session_maker
from app.db.models import User
from app.config import settings
from app.db.schemas import ObjectCheckModel, ObjectPhotoModel
my_object_router = Router()

@my_object_router.message(F.text.in_(get_all_texts('my_objects_btn')), UserInfo())
async def process_my_objects(message: Message, user_info: User):
    """Handler for displaying user's objects"""
    
    async with async_session_maker() as session:
        objects = await ObjectMemberDAO.find_user_objects(session, user_info.telegram_id)
        
        if not objects:
            await message.answer(
                get_text('no_objects', user_info.language)
            )
            return
        
        for obj in objects:
            object_text = get_text(
                'object_item',
                user_info.language,
                name=obj.name,
                description=obj.description or get_text('no_description', user_info.language)
            )
            
            await message.answer(
                text=object_text,
                parse_mode="MarkdownV2",
                reply_markup=object_keyboard(obj.id, user_info.language)
            )
    
@my_object_router.callback_query(ObjectActionCallback.filter(F.action == "docs"), UserInfo())
async def process_object_docs(callback: CallbackQuery, callback_data: ObjectActionCallback, user_info: User):
    """Handler for displaying object documents"""
    async with async_session_maker() as session:
        documents = await ObjectDocumentDAO.find_object_documents(session, callback_data.object_id)
        
        if not documents:
            await callback.message.answer(
                get_text('no_documents', user_info.language)
            )
            return

        
        for doc in documents:
            doc_text = get_text(
                'document_item',
                user_info.language,
                type=doc.document_type.value
            )
            
            await callback.message.answer_photo(
                photo=doc.file_id,
                caption=doc_text,
                parse_mode="MarkdownV2"
            )

@my_object_router.callback_query(ObjectActionCallback.filter(F.action == 'notify'), UserInfo())
async def process_notify_btn(
    callback: CallbackQuery, 
    callback_data: ObjectActionCallback, 
    user_info: User,
    state: FSMContext
):
    """Handler for notification button"""
    await state.update_data(object_id=callback_data.object_id)
    await state.set_state(NotifyObjectStates.waiting_message)
    
    await callback.message.answer(
        text=get_text('enter_notification', user_info.language)
    )


@my_object_router.message(F.text, StateFilter(NotifyObjectStates.waiting_message), UserInfo())
async def process_notification_message(message: Message, state: FSMContext, user_info: User):
    """Handler for processing notification message"""
    data = await state.get_data()
    object_id = data.get('object_id')
    
    notification_text = get_text(
        'notification_format',
        user_info.language,
        object_id= object_id,
        sender_name=user_info.user_enter_fio,
        username=f"@{user_info.username}" if user_info.username else "нет username",
        message=message.text
    )
    
    async with async_session_maker() as session:
        members = await ObjectMemberDAO.find_object_members(session, object_id)
        
        for member in members:
            if member.telegram_id != user_info.telegram_id: 
                try:
                    await message.bot.send_message(
                        chat_id=member.telegram_id,
                        text=notification_text,
                        parse_mode="MarkdownV2"
                    )
                except Exception as e:
                    continue  
    
    await message.answer(
        text=get_text('notification_sent', user_info.language)
    )
    await state.clear()

@my_object_router.callback_query(ObjectActionCallback.filter(F.action == 'photo'), UserInfo())
async def process_photo_btn(
    callback: CallbackQuery, 
    callback_data: ObjectActionCallback, 
    state: FSMContext,
    user_info: User
):
    """Handler for photo button"""
    await state.update_data(object_id=callback_data.object_id)
    await state.set_state(ObjectPhotoStates.waiting_photo)
    
    await callback.message.answer(
        text=get_text('send_object_photo', user_info.language)
    )

@my_object_router.message(F.photo, StateFilter(ObjectPhotoStates.waiting_photo), UserInfo())
async def process_object_photo(message: Message, state: FSMContext, user_info: User):
    """Handler for receiving photo"""
    await state.update_data(photo_id=message.photo[-1].file_id)
    await state.set_state(ObjectPhotoStates.waiting_description)
    
    await message.answer(
        text=get_text('enter_photo_description', user_info.language)
    )


@my_object_router.message(StateFilter(ObjectPhotoStates.waiting_description), UserInfo())
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
    
    # Send to photos group
    await message.bot.send_photo(
        chat_id=settings.TELEGRAM_GROUP_OBJECT_PHOTO,
        photo=data['photo_id'],
        caption=photo_text,
        parse_mode="MarkdownV2"
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

@my_object_router.message(~F.photo, StateFilter(ObjectPhotoStates.waiting_photo), UserInfo())
async def process_invalid_photo(message: Message, user_info: User):
    """Handler for invalid input in photo state"""
    await message.answer(
        text=get_text('send_photo_only', user_info.language)
    )

@my_object_router.callback_query(ObjectActionCallback.filter(F.action == 'checks'), UserInfo())
async def process_check_btn(
    callback: CallbackQuery,
    callback_data: ObjectActionCallback,
    state: FSMContext,
    user_info: User
):
    """Handler for check button"""
    await state.update_data(object_id=callback_data.object_id)
    await state.set_state(ObjectCheckStates.waiting_photo)
    
    await callback.message.answer(
        text=get_text('send_check_photo', user_info.language)
    )

@my_object_router.message(F.photo, StateFilter(ObjectCheckStates.waiting_photo), UserInfo())
async def process_check_photo(message: Message, state: FSMContext, user_info: User):
    """Handler for receiving check photo"""
    await state.update_data(photo_id=message.photo[-1].file_id)
    await state.set_state(ObjectCheckStates.waiting_description)
    
    await message.answer(
        text=get_text('enter_check_description', user_info.language)
    )

@my_object_router.message(StateFilter(ObjectCheckStates.waiting_description), UserInfo())
async def process_check_description(message: Message, state: FSMContext, user_info: User):
    """Handler for receiving check description"""
    await state.update_data(description=message.text)
    await state.set_state(ObjectCheckStates.waiting_amount)
    
    await message.answer(
        text=get_text('enter_check_amount', user_info.language)
    )

@my_object_router.message(StateFilter(ObjectCheckStates.waiting_amount), UserInfo())
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
        parse_mode="MarkdownV2"
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

@my_object_router.message(~F.photo, StateFilter(ObjectCheckStates.waiting_photo), UserInfo())
async def process_invalid_check_photo(message: Message, user_info: User):
    """Handler for invalid input in check photo state"""
    await message.answer(
        text=get_text('send_photo_only', user_info.language)
    )