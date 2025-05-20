from loguru import logger

from aiogram import Router,F
from aiogram.types import CallbackQuery,Message
from aiogram.fsm.context import FSMContext
from app.bot.kbds.inline_kbds import ForemanBackCallback, build_obj_list_kbd, get_foreman_objects_kbd,ObjListCallback,ForemanObjectCallback
from app.bot.common.texts import get_all_texts, get_text
from app.db.dao import ObjectMemberDAO
from app.db.database import async_session_maker

from app.bot.filters.user_info import UserInfo
from app.db.models import User

from app.bot.routers.foreman.object_logic.documents_list import documents_list_router
from app.bot.routers.foreman.object_logic.export_checks_xlxs import export_router
from app.bot.routers.foreman.object_logic.handover import handover_router
from app.bot.routers.foreman.object_logic.mass_mailing import mass_mailing_router
from app.bot.routers.foreman.object_logic.object_photo import object_photo_router
from app.bot.routers.foreman.object_logic.receipts import receipts_router
from app.bot.routers.foreman.object_logic.workers_list import workers_list_router



foreman_router = Router()
foreman_router.include_routers(documents_list_router, 
                                workers_list_router,
                                export_router,
                                handover_router, 
                                mass_mailing_router,
                                object_photo_router, 
                                receipts_router)


@foreman_router.message(F.text.in_(get_all_texts("objects_btn")), UserInfo())
async def handle_workers_callback(message:Message, user_info: User) -> None:
    async with async_session_maker() as session:
        objects = await ObjectMemberDAO.find_user_objects(session, user_info.telegram_id)
        if not objects:
            await message.answer(get_text("no_objects", user_info.language))
            return

    await message.answer(text=get_text("select_object_prompt", user_info.language), 
                                  reply_markup=build_obj_list_kbd(objects, page=0))


@foreman_router.callback_query(ObjListCallback.filter(F.action == "prev"), UserInfo())
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
    new_keyboard = build_obj_list_kbd(objects, page=new_page)
    try:
        await callback.message.edit_reply_markup(reply_markup=new_keyboard)
    except Exception as e:
        logger.error(f"Ошибка при обновлении клавиатуры (prev): {e}")
    await callback.answer()


@foreman_router.callback_query(ObjListCallback.filter(F.action == "next"), UserInfo())
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
    new_keyboard = build_obj_list_kbd(objects, page=new_page)
    try:
        await callback.message.edit_reply_markup(reply_markup=new_keyboard)
    except Exception as e:
        logger.error(f"Ошибка при обновлении клавиатуры (next): {e}")
    await callback.answer()


@foreman_router.callback_query(ObjListCallback.filter(F.action == "back"), UserInfo())
async def handle_back(callback: CallbackQuery, callback_data: ObjListCallback, user_info:User) -> None:
    """
    Обработчик для кнопки "Back".
    Возвращает пользователя к главному меню прораба, обновляя сообщение.
    """
    main_text = get_text("select_object_prompt", user_info.language)
    main_keyboard = get_foreman_objects_kbd(user_info.language)
    try:
        await callback.message.edit_text(text=main_text, reply_markup=main_keyboard)
    except Exception as e:
        logger.error(f"Ошибка при обновлении сообщения для кнопки 'back': {e}")
    await callback.answer()


@foreman_router.callback_query(ObjListCallback.filter(F.action == "select"), UserInfo())
async def handle_select_object(callback: CallbackQuery, callback_data: ObjListCallback, user_info: User) -> None:
    await callback.message.delete()
    await callback.message.answer(get_text("select_object_action", user_info.language),
                                  reply_markup=get_foreman_objects_kbd(object_id=callback_data.id, lang=user_info.language))
    

@foreman_router.callback_query(ForemanObjectCallback.filter(F.action == "back"), UserInfo())
async def handle_back_btn_after_select_obj(callback: CallbackQuery, callback_data: ForemanObjectCallback, user_info: User) -> None:
    async with async_session_maker() as session:
        objects = await ObjectMemberDAO.find_user_objects(session, user_info.telegram_id)
        if not objects:
            await callback.message.answer(get_text("no_objects", user_info.language))
            return

    await callback.message.delete()
    await callback.message.answer(get_text("select_object_action", user_info.language),
                                  reply_markup=build_obj_list_kbd(objects, page=0))

@foreman_router.callback_query(ForemanBackCallback.filter(), UserInfo())
async def process_back_btn(
    callback: CallbackQuery,
    callback_data: ForemanBackCallback,
    state: FSMContext,
    user_info: User
) -> None:
    """
    Обработчик нажатия кнопки "Назад".
    Возвращает пользователя в предыдущее состояние.
    """
    await callback.message.delete()
    await state.clear()
    await callback.message.answer(
        text=get_text("select_object_action", user_info.language),reply_markup=get_foreman_objects_kbd(
            object_id=callback_data.object_id,
            lang=user_info.language,
        )
    )