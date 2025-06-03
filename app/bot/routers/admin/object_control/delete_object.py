from aiogram import Router,F
from aiogram.types import Message,CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from loguru import logger

from app.bot.common.states import AdminPanelStates
from app.bot.common.texts import get_all_texts, get_text
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import ObjListCallback, build_obj_list_kbd
from app.db.dao import ObjectDAO, ObjectMemberDAO
from app.db.database import async_session_maker
from app.db.models import User,Object
from app.db.schemas import ObjectFilterModel

delete_object = Router()

@delete_object.message(F.text.in_(get_all_texts('delete_object_btn')), StateFilter(AdminPanelStates.objects_control),UserInfo())
async def process_delete_obj_btn(message:Message,state:FSMContext,user_info:User):
    async with async_session_maker() as session:
        objects = await ObjectMemberDAO.find_all(session, ObjectFilterModel())
        if not objects:
            await message.answer(get_text("no_objects", user_info.language))
            return
    await message.delete()
    await message.answer(
        text=get_text("add_worker_to_object_text", user_info.language),
        reply_markup=build_obj_list_kbd(objects, context=('delete_object'))
    )

@delete_object.callback_query(ObjListCallback.filter(F.action == "select", F.context == "delete_object"), UserInfo())
async def process_delete_obj(callback: CallbackQuery, callback_data: ObjListCallback,state:FSMContext, user_info: User):
    await callback.message.delete()
    async with async_session_maker() as session:
        deleted_object:Object = await ObjectDAO.find_one_or_none(session,ObjectFilterModel(id = callback_data.id))
        await ObjectDAO.delete(session,ObjectFilterModel.model_validate(deleted_object.to_dict()))
    await callback.message.answer(get_text('object_has_been_deleted', object_id = callback_data.id))