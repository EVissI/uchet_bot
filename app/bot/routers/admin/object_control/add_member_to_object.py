from aiogram import Router,F
from aiogram.types import Message,CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from app.bot.common.fsm_managment import DialogMessageManager, StateHistoryMixin
from app.bot.common.states import AdminAddMemberToObjectStates, AdminPanelStates
from app.bot.common.texts import get_text,get_all_texts
from app.bot.kbds.markup_kbds import AdminObjectControlKeyboard
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import ObjListCallback, build_paginated_list_kbd
from app.bot.kbds.markup_kbds import get_back_keyboard
from app.db.database import async_session_maker
from app.db.schemas import ObjectFilterModel,ObjectMemberModel
from app.db.dao import ObjectMemberDAO, UserDAO
from app.db.models import User

class AddMemberToObjectRouter(Router, StateHistoryMixin, DialogMessageManager):
    def __init__(self):
        super().__init__()

add_member_to_object_router = Router()

@add_member_to_object_router.message(F.text.in_(get_all_texts("add_worker_to_object_btn")),
                              StateFilter(AdminPanelStates.objects_control),
                              UserInfo())
async def add_member_to_object_handler(message: Message, user_info: User):
    async with async_session_maker() as session:
        objects = await ObjectMemberDAO.find_all(session, ObjectFilterModel())
        if not objects:
            await message.answer(get_text("no_objects", user_info.language))
            return
    await message.delete()
    await message.answer(
        text=get_text("add_worker_to_object_text", user_info.language),
        reply_markup=build_paginated_list_kbd(objects,context=('add_member_to_object'))
    )


@add_member_to_object_router.callback_query(ObjListCallback.filter(F.action == "select" and F.context == "add_member_to_object"), UserInfo())
async def select_object_for_adding_member(callback: CallbackQuery, callback_data: ObjListCallback,state:FSMContext, user_info: User):
    """Handler for selecting an object to add a member."""
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(
        text=get_text("add_worker_to_object_w8_ids", user_info.language, object_name=callback_data.object_name),
        reply_markup=get_back_keyboard(user_info.language)
    )
    await state.update_data(object_id=callback_data.object_id)
    await state.set_state(AdminAddMemberToObjectStates.waiting_user_ids)

@add_member_to_object_router.message(F.text, StateFilter(AdminAddMemberToObjectStates.waiting_user_ids), UserInfo())
async def process_user_ids(message: Message, state: FSMContext, user_info: User):
    """Handler for processing user IDs to add to an object."""
    user_ids = message.text.split(',')
    user_ids = [uid.strip() for uid in user_ids if uid.strip().isdigit()]
    
    if not user_ids:
        await message.delete()
        await message.answer(get_text("no_valid_user_ids", user_info.language),
                            reply_markup=AdminObjectControlKeyboard.build_object_control_kb(user_info.language))
        return
    
    data = await state.get_data()
    object_id = data.get('object_id')
    
    async with async_session_maker() as session:
        users = []
        for user_id in user_ids:
            user = await UserDAO.find_by_telegram_id(session, int(user_id))
            if user:
                users.append(ObjectMemberModel(
                    object_id=object_id,
                    user_id=user.id,
                ))
        if not users:
            await message.delete()
            await message.answer(get_text("no_valid_users_found", user_info.language),
                                 reply_markup=AdminObjectControlKeyboard.build_object_control_kb(user_info.language)
                                 )
            return
        for user_id in user_ids:
            await ObjectMemberDAO.add_many(session,users)
    
    await message.answer(get_text("members_added_successfully", user_info.language),
                        await message.delete(),
                        reply_markup=AdminObjectControlKeyboard.build_object_control_kb(user_info.language))
    await state.clear()