﻿from aiogram import F,Router
from aiogram.types import CallbackQuery

from loguru import logger

from app.bot.filters.role_filter import RoleFilter
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import ObjListCallback
from app.bot.common.texts import get_text
from app.bot.kbds.inline_kbds import build_paginated_list_kbd
from app.db.dao import ObjectMemberDAO
from app.db.database import async_session_maker
from app.db.schemas import ObjectFilterModel
from app.db.models import User

from app.bot.routers.admin.object_control.setup_object_control import setup_object_control_router
from app.bot.routers.admin.material_reminder.setup import reminder_setup_router
from app.bot.routers.admin.notify.notify_router import admin_notify_router
from app.bot.routers.admin.tools_control.setup_tools_control import setup_tools_control_router
from app.bot.routers.admin.generate_file_id import generate_file_id_router
from app.bot.routers.admin.cheks_object import admin_reminder_object_router


main_admin_router = Router()
main_admin_router.message.filter(RoleFilter(User.Role.admin.value))
main_admin_router.include_routers(setup_object_control_router,
                                  reminder_setup_router,
                                  admin_notify_router,
                                  setup_tools_control_router,
                                  generate_file_id_router,
                                  admin_reminder_object_router
                                  )

@main_admin_router.callback_query(ObjListCallback.filter(F.action == "prev"), UserInfo())
async def handle_prev_page(callback: CallbackQuery, callback_data: ObjListCallback, user_info:User) -> None:
    """
    Обработчик для кнопки "←" (prev).
    Вычисляет новую страницу (page - 1), получает список объектов и обновляет клавиатуру.
    """
    new_page = callback_data.page - 1 if callback_data.page > 0 else 0
    async with async_session_maker() as session:
        objects = await ObjectMemberDAO.find_all(session, ObjectFilterModel())
        if not objects:
            await callback.message.answer(get_text("no_objects", user_info.language))
            return
    new_keyboard = build_paginated_list_kbd(objects, page=new_page,context=callback_data.context)
    try:
        await callback.message.edit_reply_markup(reply_markup=new_keyboard)
    except Exception as e:
        logger.error(f"Ошибка при обновлении клавиатуры (prev): {e}")
    await callback.answer()


@main_admin_router.callback_query(ObjListCallback.filter(F.action == "next"), UserInfo())
async def handle_next_page(callback: CallbackQuery, callback_data: ObjListCallback, user_info:User) -> None:
    """
    Обработчик для кнопки "→" (next).
    Вычисляет новую страницу (page + 1), получает список объектов и обновляет клавиатуру.
    """
    new_page = callback_data.page + 1
    async with async_session_maker() as session:
        objects = await ObjectMemberDAO.find_all(session, ObjectFilterModel())
        if not objects:
            await callback.message.answer(get_text("no_objects", user_info.language))
            return
    new_keyboard = build_paginated_list_kbd(objects, page=new_page,context=callback_data.context)
    try:
        await callback.message.edit_reply_markup(reply_markup=new_keyboard)
    except Exception as e:
        logger.error(f"Ошибка при обновлении клавиатуры (next): {e}")
    await callback.answer()
