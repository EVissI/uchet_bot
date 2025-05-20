from loguru import logger

from aiogram import Router,F
from aiogram.types import CallbackQuery

from app.bot.common.texts import get_text
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import ForemanObjectCallback
from app.db.dao import ObjectDAO, ObjectMemberDAO
from app.db.schemas import ObjectFilterModel
from app.db.models import User    
from app.db.database import async_session_maker

workers_list_router = Router()

@workers_list_router.callback_query(ForemanObjectCallback.filter(F.action == "workers"), UserInfo())
async def handle_workers_list(callback: CallbackQuery, callback_data: ForemanObjectCallback, user_info: User) -> None:
    object_id = callback_data.object_id

    async with async_session_maker() as session:
        members: list[User] = await ObjectMemberDAO.find_object_members(session, object_id)
        selected_object = await ObjectDAO.find_one_or_none(session, ObjectFilterModel(id=object_id))

        if not members:
            await callback.message.answer(get_text("no_object_members", user_info.language))
            await callback.answer()
            return

        object_name = selected_object.name if selected_object else "неизвестный объект"
        await callback.message.delete()
        for member in members:
            username = f"@{member.username}" if member.username else "нет username"
            worker_text = get_text(
                "worker_info_format",
                user_info.language,
                telegram_id=member.telegram_id,
                username=username,
                full_name=member.user_enter_fio,
                phone=member.phone_number,
                status=member.role,
                object_name=object_name
            )
            try:
                await callback.message.answer(text=worker_text)
            except Exception as e:
                logger.error(f"Ошибка при отправке сообщения рабочего: {e}")
        await callback.answer()