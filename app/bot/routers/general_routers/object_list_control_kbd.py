from aiogram import Router,F
from aiogram.types import CallbackQuery
from loguru import logger
from app.bot.common.texts import get_text
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import ObjListCallback, build_paginated_list_kbd
from app.db.dao import ObjectMemberDAO, ObjectDAO
from app.db.database import async_session_maker
from app.db.models import User
from app.db.schemas import ObjectFilterModel

kbd_obj_list_router = Router()

@kbd_obj_list_router.callback_query(ObjListCallback.filter((F.action == "prev") & (F.object_type == 'all_objects')), UserInfo())
async def handle_prev_page(callback: CallbackQuery, callback_data: ObjListCallback, user_info:User) -> None:
    """
    Обработчик для кнопки "←" (prev).
    Вычисляет новую страницу (page - 1), получает список объектов и обновляет клавиатуру.
    """
    new_page = callback_data.page - 1 if callback_data.page > 0 else 0
    async with async_session_maker() as session:
        objects = await ObjectDAO.find_all(session, ObjectFilterModel(is_active=True))
        if not objects:
            await callback.message.answer(get_text("no_objects", user_info.language))
            return
    new_keyboard = build_paginated_list_kbd(objects, page=new_page, context=callback_data.context)
    try:
        await callback.message.edit_reply_markup(reply_markup=new_keyboard)
    except Exception as e:
        logger.error(f"Ошибка при обновлении клавиатуры (prev): {e}")
    await callback.answer()


@kbd_obj_list_router.callback_query(ObjListCallback.filter((F.action == "next") & (F.object_type == 'all_objects')), UserInfo())
async def handle_next_page(callback: CallbackQuery, callback_data: ObjListCallback, user_info:User) -> None:
    """
    Обработчик для кнопки "→" (next).
    Вычисляет новую страницу (page + 1), получает список объектов и обновляет клавиатуру.
    """
    new_page = callback_data.page + 1
    async with async_session_maker() as session:
        objects = await ObjectMemberDAO.find_user_objects(session, user_info.telegram_id)
        if not objects:
            await callback.message.answer(get_text("no_objects", user_info.language))
            return
    new_keyboard = build_paginated_list_kbd(objects, 
                                            page=new_page, 
                                            context=callback_data.context, 
                                            object_type=callback_data.object_type)
    try:
        await callback.message.edit_reply_markup(reply_markup=new_keyboard)
    except Exception as e:
        logger.error(f"Ошибка при обновлении клавиатуры (next): {e}")
    await callback.answer()


@kbd_obj_list_router.callback_query(ObjListCallback.filter((F.action == "prev") & (F.object_type == 'object')), UserInfo())
async def handle_prev_page(callback: CallbackQuery, callback_data: ObjListCallback, user_info:User) -> None:
    """
    Обработчик для кнопки "←" (prev).
    Вычисляет новую страницу (page - 1), получает список объектов и обновляет клавиатуру.
    """
    new_page = callback_data.page - 1 if callback_data.page > 0 else 0
    async with async_session_maker() as session:
        objects = await ObjectMemberDAO.find_user_objects(session, user_info.telegram_id)
        if not objects:
            await callback.message.answer(get_text("no_objects", user_info.language))
            return
    new_keyboard = build_paginated_list_kbd(objects, 
                                            page=new_page,
                                            context=callback_data.context,
                                            object_type=callback_data.object_type)
    try:
        await callback.message.edit_reply_markup(reply_markup=new_keyboard)
    except Exception as e:
        logger.error(f"Ошибка при обновлении клавиатуры (prev): {e}")
    await callback.answer()


@kbd_obj_list_router.callback_query(ObjListCallback.filter((F.action == "next") & (F.object_type == 'object')), UserInfo())
async def handle_next_page(callback: CallbackQuery, callback_data: ObjListCallback, user_info:User) -> None:
    """
    Обработчик для кнопки "→" (next).
    Вычисляет новую страницу (page + 1), получает список объектов и обновляет клавиатуру.
    """
    new_page = callback_data.page + 1
    async with async_session_maker() as session:
        objects = await ObjectMemberDAO.find_user_objects(session, user_info.telegram_id)
        if not objects:
            await callback.message.answer(get_text("no_objects", user_info.language))
            return
    new_keyboard = build_paginated_list_kbd(objects, page=new_page,context=callback_data.context)
    try:
        await callback.message.edit_reply_markup(reply_markup=new_keyboard)
    except Exception as e:
        logger.error(f"Ошибка при обновлении клавиатуры (next): {e}")
    await callback.answer()


@kbd_obj_list_router.callback_query(ObjListCallback.filter((F.action == "prev") & (F.object_type == 'object_workers')), UserInfo())
async def handle_prev_page(callback: CallbackQuery, callback_data: ObjListCallback, user_info:User) -> None:
    """
    Обработчик для кнопки "←" (prev).
    Вычисляет новую страницу (page - 1), получает список объектов и обновляет клавиатуру.
    """
    new_page = callback_data.page - 1 if callback_data.page > 0 else 0
    async with async_session_maker() as session:
        workers = await ObjectMemberDAO.find_object_members(session, callback_data.sub_info)
        if not workers:
            await callback.message.answer(get_text("no_objects", user_info.language))
            return
        new_keyboard = build_paginated_list_kbd(workers, 
                                                page=new_page, 
                                                context=callback_data.context, 
                                                object_type=callback_data.object_type,
                                                text_field='user_enter_fio',
                                                primary_key_name='telegram_id',
                                                sub_info=callback_data.sub_info)
        try:
            await callback.message.edit_reply_markup(reply_markup=new_keyboard)
        except Exception as e:
            logger.error(f"Ошибка при обновлении клавиатуры (prev): {e}")
        await callback.answer()


@kbd_obj_list_router.callback_query(ObjListCallback.filter((F.action == "next") & (F.object_type == 'object_workers')), UserInfo())
async def handle_next_page(callback: CallbackQuery, callback_data: ObjListCallback, user_info:User) -> None:
    """
    Обработчик для кнопки "→" (next).
    Вычисляет новую страницу (page + 1), получает список объектов и обновляет клавиатуру.
    """
    new_page = callback_data.page + 1
    async with async_session_maker() as session:
        workers = await ObjectMemberDAO.find_object_members(session, callback_data.sub_info)
        if not workers:
            await callback.message.answer(get_text("no_objects", user_info.language))
            return
        new_keyboard = build_paginated_list_kbd(workers, 
                                                page=new_page, 
                                                context=callback_data.context, 
                                                object_type=callback_data.object_type,
                                                text_field='user_enter_fio',
                                                primary_key_name='telegram_id',
                                                sub_info=callback_data.sub_info)
        try:
            await callback.message.edit_reply_markup(reply_markup=new_keyboard)
        except Exception as e:
            logger.error(f"Ошибка при обновлении клавиатуры (prev): {e}")
        await callback.answer()