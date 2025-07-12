from aiogram import Router,F
from aiogram.types import Message, CallbackQuery,BufferedInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from loguru import logger
from app.bot.common.excel.utils import create_workers_full_info_excel
from app.bot.common.states import AdminPanelStates
from app.bot.common.texts import get_text, get_all_texts
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import ObjListCallback, ObjectViewCallback, ObjectWorkersViewCallback, build_paginated_list_kbd, get_object_view_kbd, get_object_workers_view_kbd
from app.db.models import Object, ObjectDocument, User
from app.db.dao import ObjectDAO, ObjectDocumentDAO, UserDAO
from app.db.database import async_session_maker
from app.db.schemas import ObjectFilterModel


view_object_router = Router()


@view_object_router.message(F.text.in_(get_all_texts('view_object')),
                            StateFilter(AdminPanelStates.objects_control), 
                            UserInfo())
async def process_view_object(message:Message, state:FSMContext, user_info: User):
    async with async_session_maker() as session:
        objects:list[Object] = await ObjectDAO.find_all(session, ObjectFilterModel())
        if not objects:
            await message.answer(get_text("no_objects", user_info.language))
            return
    await message.answer(
        text=get_text("select_object_prompt", user_info.language),
        reply_markup=build_paginated_list_kbd(objects, context=('view_object'))
    )


@view_object_router.callback_query(ObjListCallback.filter((F.action == "select") & (F.context == "view_object")), UserInfo())
async def process_view_object_callback(callback: CallbackQuery, callback_data: ObjListCallback, state:FSMContext, user_info: User):
    await callback.message.delete()
    async with async_session_maker() as session:
        selected_object:Object = await ObjectDAO.find_one_or_none(session, ObjectFilterModel(id=callback_data.id))
        if not selected_object:
            await callback.answer(get_text("object_not_found", user_info.language), show_alert=True)
            return
        
        text = get_text(
            "object_data_format",
            user_info.language,
            name=selected_object.name,
            description=selected_object.description or "-",
            is_active="🟢" if selected_object.is_active else "🔴",
        )
        await callback.message.answer(
            text=get_text("object_data_header", user_info.language) + "\n\n" + text,
            reply_markup=get_object_view_kbd(selected_object.id, selected_object.is_active, user_info.language)  
        )


@view_object_router.callback_query(ObjectViewCallback.filter(F.action == "back"), UserInfo())
async def process_back_to_object_list(callback: CallbackQuery, user_info: User):
    await callback.message.delete()
    async with async_session_maker() as session:
        objects:list[Object] = await ObjectDAO.find_all(session, ObjectFilterModel())
        if not objects:
            await callback.message.answer(get_text("no_objects", user_info.language))
            return
    await callback.message.answer(
        text=get_text("select_object_prompt", user_info.language),
        reply_markup=build_paginated_list_kbd(objects, context=('view_object'))
    )


@view_object_router.callback_query(ObjectViewCallback.filter(F.action == "documents"), UserInfo())
async def process_view_object_documents(callback: CallbackQuery, callback_data: ObjectViewCallback, user_info: User):
    """Handle viewing object documents"""
    async with async_session_maker() as session:
        documents:list[ObjectDocument] = await ObjectDocumentDAO.find_object_documents(session, callback_data.object_id, user_info.role)
        selected_object:Object = await ObjectDAO.find_one_or_none(session, filters=ObjectFilterModel(id=callback_data.object_id))
        if not documents:
            await callback.message.answer(get_text("no_object_documents", user_info.language))
            await callback.answer()
            return
        if not selected_object:
            await callback.answer(get_text("object_not_found", user_info.language), show_alert=True)
            return
        
        object_name = selected_object.name if selected_object else "неизвестный объект"
        for document in documents:
            if document.file_id:
                try:
                    if document.document_type == ObjectDocument.DocumentFileType.photo.value:
                        await callback.message.answer_photo(
                            document.file_id,
                            caption=get_text("document_info_format", user_info.language,
                                            document_type=document.document_type,
                                            object_name=object_name)
                        )
                    if document.document_type == ObjectDocument.DocumentFileType.pdf.value:
                        await callback.message.answer_document(
                            document.file_id,
                            caption=get_text("document_info_format", user_info.language,
                                            document_type=document.document_type,
                                            object_name=object_name)
                        )
                except Exception as e:
                    logger.error(f"Ошибка при отправке сообщения документа: {e}")
        await callback.answer()

@view_object_router.callback_query(ObjectViewCallback.filter(F.action == "activate_deactivate"), UserInfo())
async def process_activate_deactivate_object(callback: CallbackQuery, callback_data: ObjectViewCallback, user_info: User):
    """Handle activating or deactivating an object"""
    async with async_session_maker() as session:
        selected_object:Object = await ObjectDAO.find_one_or_none(session, ObjectFilterModel(id=callback_data.object_id))
        if not selected_object:
            await callback.answer(get_text("object_not_found", user_info.language), show_alert=True)
            return
        
        new_status = not selected_object.is_active
        selected_object.is_active = new_status
        await ObjectDAO.update(session, 
                               ObjectFilterModel(id=callback_data.object_id),
                               ObjectFilterModel.model_validate(selected_object.to_dict()))
    async with async_session_maker() as session:
        selected_object:Object = await ObjectDAO.find_one_or_none(session, ObjectFilterModel(id=callback_data.object_id))
        if not selected_object:
            await callback.answer(get_text("object_not_found", user_info.language), show_alert=True)
            return
        text = get_text(
            "object_data_format",
            user_info.language,
            name=selected_object.name,
            description=selected_object.description or "-",
            is_active="🟢" if selected_object.is_active else "🔴",
        )
        await callback.message.edit_text(
            text=get_text("object_data_header", user_info.language) + "\n\n" + text,
            reply_markup=get_object_view_kbd(selected_object.id, selected_object.is_active, user_info.language)  
        )
        await callback.answer()

@view_object_router.callback_query(ObjectViewCallback.filter(F.action == "workers"), UserInfo())
async def process_view_object_workers(callback: CallbackQuery, callback_data: ObjectViewCallback, user_info: User):
    await callback.message.delete()
    await callback.message.answer(text=get_text("select_worker_role", user_info.language),
                                  reply_markup=get_object_workers_view_kbd(callback_data.object_id, user_info.language))
    
@view_object_router.callback_query(ObjectWorkersViewCallback.filter(F.role == "back"), UserInfo())
async def process_back_to_object_view(callback: CallbackQuery,callback_data:ObjectWorkersViewCallback, user_info: User):
    await callback.message.delete()
    async with async_session_maker() as session:
        selected_object:Object = await ObjectDAO.find_one_or_none(session, ObjectFilterModel(id=callback_data.object_id))
        if not selected_object:
            await callback.answer(get_text("object_not_found", user_info.language), show_alert=True)
            return
        
        text = get_text(
            "object_data_format",
            user_info.language,
            name=selected_object.name,
            description=selected_object.description or "-",
            is_active="🟢" if selected_object.is_active else "🔴",
        )
        await callback.message.answer(
            text=get_text("object_data_header", user_info.language) + "\n\n" + text,
            reply_markup=get_object_view_kbd(selected_object.id, selected_object.is_active, user_info.language)  
        )

@view_object_router.callback_query(ObjectWorkersViewCallback.filter(), UserInfo())
async def process_back_to_object_view(callback: CallbackQuery,callback_data:ObjectWorkersViewCallback, user_info: User):
    """Handle viewing workers for an object"""
    await callback.message.delete()
    async with async_session_maker() as session:
        workers:list[User] = await UserDAO.get_workers_with_related(session, 
                                                                    callback_data.role, 
                                                                    callback_data.object_id)
        if not workers:
            selected_object:Object = await ObjectDAO.find_one_or_none(session, ObjectFilterModel(id=callback_data.object_id))
            await callback.message.answer(get_text("no_object_members", user_info.language))
            text = get_text(
                "object_data_format",
                user_info.language,
                name=selected_object.name,
                description=selected_object.description or "-",
                is_active="🟢" if selected_object.is_active else "🔴",
            )
            await callback.message.answer(
                text=get_text("object_data_header", user_info.language) + "\n\n" + text,
                reply_markup=get_object_view_kbd(selected_object.id, selected_object.is_active, user_info.language)  
            )
            return
        excel_file = create_workers_full_info_excel(workers)
        await callback.message.answer_document(
            document=BufferedInputFile(
                excel_file.getvalue(),
                filename=f"workers_{callback.message.date.strftime('%d_%m_%Y')}.xlsx"
            ),
        )