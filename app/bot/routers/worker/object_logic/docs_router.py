from aiogram import Router,F
from aiogram.types import CallbackQuery

from app.bot.common.texts import get_text
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import WorkerObjectActionCallback
from app.db.dao import ObjectDocumentDAO
from app.db.database import async_session_maker
from app.db.models import User
worker_docs_router = Router()


@worker_docs_router.callback_query(WorkerObjectActionCallback.filter(F.action == "docs"), UserInfo())
async def process_object_docs(callback: CallbackQuery, callback_data: WorkerObjectActionCallback, user_info: User):
    """Handler for displaying object documents"""
    await callback.message.delete()
    async with async_session_maker() as session:
        documents = await ObjectDocumentDAO.find_object_documents(session, callback_data.object_id, user_info.role)
        
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
            )
    await callback.answer()