from aiogram import Router,F
from aiogram.types import Message,CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from loguru import logger
from app.bot.common.fsm_managment import DialogMessageManager, StateHistoryMixin
from app.bot.common.states import AdminAddMemberToObjectStates, AdminPanelStates
from app.bot.common.texts import get_text,get_all_texts
from app.bot.kbds.markup_kbds import AdminObjectControlKeyboard
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import ObjListCallback, build_paginated_list_kbd
from app.bot.kbds.markup_kbds import get_back_keyboard
from app.db.database import async_session_maker
from app.db.schemas import ObjectFilterModel,ObjectMemberModel
from app.db.dao import ObjectMemberDAO, UserDAO,ObjectDAO
from app.db.models import Object, User

class AddMemberToObjectRouter(Router, StateHistoryMixin, DialogMessageManager):
    def __init__(self):
        super().__init__()

add_member_to_object_router = AddMemberToObjectRouter()

@add_member_to_object_router.message(F.text.in_(get_all_texts("add_worker_to_object_btn")),
                              StateFilter(AdminPanelStates.objects_control),
                              UserInfo())
async def process_add_worker_to_object_btn(message: Message, user_info: User):
    await message.delete()
    async with async_session_maker() as session:
        objects = await ObjectDAO.find_all(session, ObjectFilterModel())
        if not objects:
            await message.answer(get_text("no_objects", user_info.language))
            return
    await message.answer(
        text=get_text("add_worker_to_object_text", user_info.language),
        reply_markup=build_paginated_list_kbd(objects, context=('add_member_to_object'))
    )


@add_member_to_object_router.callback_query(ObjListCallback.filter((F.action == "select") 
                                                                   & (F.context == "add_member_to_object")), UserInfo())
async def select_object_for_adding_member(callback: CallbackQuery, callback_data: ObjListCallback,state:FSMContext, user_info: User):
    """Handler for selecting an object to add a member."""
    await callback.answer()
    await callback.message.delete()
    async with async_session_maker() as session:
        object:Object = await ObjectDAO.find_one_or_none(session, filters=ObjectFilterModel(id = callback_data.id))
        bot_message = await callback.message.answer(
            text=get_text("add_worker_to_object_w8_ids", user_info.language, object_name=object.name),
            reply_markup=get_back_keyboard(user_info.language)
        )
        await add_member_to_object_router.save_message(state,bot_message.message_id)
    await state.update_data(object_id=callback_data.id)
    await state.set_state(AdminAddMemberToObjectStates.waiting_user_ids)


@add_member_to_object_router.message(F.text.in_(get_all_texts('back_btn')),
                                    StateFilter(AdminAddMemberToObjectStates.waiting_user_ids),
                                    UserInfo())
async def back_btn(message:Message, state:FSMContext, user_info:User):
    await add_member_to_object_router.save_message(state,message.message_id)
    await add_member_to_object_router.clear_messages(state, message.chat.id, message.bot)
    await state.set_state(AdminPanelStates.objects_control)
    async with async_session_maker() as session:
        objects = await ObjectDAO.find_all(session, ObjectFilterModel())
        if not objects:
            await message.answer(get_text("no_objects", user_info.language))
            return
    bot_message = await message.answer(
        text=get_text("add_worker_to_object_text", user_info.language),
        reply_markup=build_paginated_list_kbd(objects,context=('add_member_to_object'))
    )
    await add_member_to_object_router.save_message(bot_message.message_id)


@add_member_to_object_router.message(F.text, 
                                    StateFilter(AdminAddMemberToObjectStates.waiting_user_ids),
                                    UserInfo())
async def process_user_ids(message: Message, state: FSMContext, user_info: User):
    """Handler for processing user IDs to add to an object."""
    user_ids = message.text.split(',')
    user_ids = [uid.strip() for uid in user_ids if uid.strip().isdigit()]
    
    if not user_ids:
        bot_message = await message.answer(
            get_text("no_valid_user_ids", user_info.language),
            reply_markup=AdminObjectControlKeyboard.build_object_control_kb(user_info.language)
        )
        add_member_to_object_router.save_message(state,bot_message.message_id)
        return
    
    data = await state.get_data()
    object_id = data.get('object_id')
    
    success_count = 0
    failed_count = 0
    failed_reasons = {}
    
    async with async_session_maker() as session:
        object_members:list[User] = await ObjectMemberDAO.find_object_members(session, object_id)
        object_info:Object = await ObjectDAO.find_one_or_none(session, filters=ObjectFilterModel(id=object_id))
        add_users = []
        for user_id in user_ids:
            try:
                user_id = int(user_id)
                user = await UserDAO.find_by_telegram_id(session, user_id)

                if not user:
                    failed_count += 1
                    failed_reasons[user_id] = "Пользователь не найден"
                    continue
                
                if user in object_members:
                    failed_count += 1
                    failed_reasons[user_id] = f"Уже добавлен на объект ({user.user_enter_fio})"
                    continue
                
                 
                add_users.append(ObjectMemberModel(
                        object_id=object_id,
                        user_id=user.telegram_id
                    )
                )
                success_count += 1
                await message.bot.send_message(user.telegram_id,text=get_text(
                        "added_to_object_notification",
                        user.language,
                        object_name=object_info.name,
                    ))
            except Exception as e:
                logger.error(f"Error adding user {user_id}: {e}")
                failed_count += 1
                failed_reasons[user_id] = "Ошибка при добавлении"
        await ObjectMemberDAO.add_many(session, add_users)
        failed_text = "\n".join(
            f"• ID {user_id}: {reason}" 
            for user_id, reason in failed_reasons.items()
        ) if failed_reasons else "Нет"

        await message.answer(
            get_text(
                "members_added_successfully",
                user_info.language,
                success_count=success_count,
                failed_count=failed_count,
                failed_reasons=failed_text
            ),
            reply_markup=AdminObjectControlKeyboard.build_object_control_kb(user_info.language)
        )
        await add_member_to_object_router.clear_messages(state, message.chat.id, message.bot)
        await state.set_state(AdminPanelStates.objects_control)