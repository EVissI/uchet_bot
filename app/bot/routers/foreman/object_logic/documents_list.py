from loguru import logger

from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.bot.common.texts import get_text
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import ForemanObjectCallback
from app.db.dao import ObjectDAO, ObjectDocumentDAO
from app.db.models import User, ObjectDocument,Object
from app.db.schemas import ObjectFilterModel
from app.db.database import async_session_maker

documents_list_router = Router()

@documents_list_router.callback_query(ForemanObjectCallback.filter(F.action == "documentation"), UserInfo())
async def handle_workers_list(callback: CallbackQuery, callback_data: ForemanObjectCallback, user_info: User) -> None:
    object_id = callback_data.object_id

    async with async_session_maker() as session:
        documents:list[ObjectDocument] = await ObjectDocumentDAO.find_object_documents(session, object_id, user_info.role)
        logger.info(f"documents: {documents}")
        selected_object:Object = await ObjectDAO.find_one_or_none(session, filters=ObjectFilterModel(id=object_id))

        if not documents:
            await callback.message.answer(get_text("no_object_documents", user_info.language))
            await callback.answer()
            return

        object_name = selected_object.name if selected_object else "неизвестный объект"

        await callback.message.delete()
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