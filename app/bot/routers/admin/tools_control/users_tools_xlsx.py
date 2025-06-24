from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.bot.common.excel.utils import create_user_tools_report
from app.bot.common.states import AdminPanelStates
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import ObjListCallback, build_paginated_list_kbd
from app.db.dao import ObjectDAO, ObjectMemberDAO, UserDAO, ToolDAO
from app.db.schemas import ObjectFilterModel, ToolFilterModel
from app.db.models import User
from app.bot.common.texts import get_text,get_all_texts
from app.db.database import async_session_maker

users_tools_xlsx_router = Router()


@users_tools_xlsx_router.message(F.text.startswith("/user_tools_xlsx"),
                                 StateFilter(AdminPanelStates.tools_control),
                                 UserInfo())
async def user_tools_xlsx_command(message: Message,user_info:User):
    """
    Команда для выгрузки инструментов по конкретному пользователю.
    Формат: /user_tools_xlsx <user_id>
    """
    args = message.text.split()
    if len(args) < 2:
        await message.reply("Укажите ID пользователя: /user_tools_xlsx <user_id>")
        return

    try:
        user_id = int(args[1])
    except ValueError:
        await message.reply("ID пользователя должен быть числом.")
        return

    lang = user_info.language
    async with async_session_maker() as session:
        user = await UserDAO.find_by_telegram_id(session, user_id)
        if not user:
            await message.reply(get_text("no_users_found", lang))
            return

        tools = await ToolDAO.find_all(session, ToolFilterModel(user_id=user_id))
        if not tools:
            await message.reply(get_text("user_has_no_tools", lang))
            return

        xlsx_file = create_user_tools_report(tools, user, lang)
        input_file = BufferedInputFile(xlsx_file.getvalue(), filename=f"tools_{user.user_enter_fio}.xlsx")
        await message.answer_document(
            document=input_file,
            caption=get_text("user_tools_list", lang, full_name=user.user_enter_fio)
        )

@users_tools_xlsx_router.message(F.text.in_(get_all_texts('user_tools_list_btn')),
                                 StateFilter(AdminPanelStates.tools_control),
                                 UserInfo())
async def process_user_tools_list_markup_btn(message:Message,state:FSMContext, user_info:User):
    async with async_session_maker() as session:
        objects = await ObjectDAO.find_all(session,ObjectFilterModel())
        if not objects:
            await message.answer(get_text("no_objects_found", user_info.language))
            return
        await message.answer(
            get_text("objects_list", user_info.language),
            reply_markup=build_paginated_list_kbd(objects, context="user_tools", object_type='all_objects')
        )

@users_tools_xlsx_router.callback_query(ObjListCallback.filter((F.context == "user_tools") 
                                                               &(F.action == "select") 
                                                               &(F.object_type=='all_objects')),UserInfo())
async def process_object_select_for_workers(callback: CallbackQuery, callback_data: ObjListCallback, user_info: User):
    async with async_session_maker() as session:
        workers = await ObjectMemberDAO.find_object_members(session, callback_data.id)
        if not workers:
            await callback.message.edit_text(get_text("no_object_members", user_info.language))
            return
        await callback.message.edit_text(
            get_text("object_members_header", user_info.language),
            reply_markup=build_paginated_list_kbd(workers,
                                            context='user_tools',
                                            sub_info=callback_data.id,
                                            text_field='user_enter_fio',
                                            primary_key_name='telegram_id',
                                            object_type='object_workers',
                                            page=0)
        )

@users_tools_xlsx_router.callback_query(ObjListCallback.filter((F.context == "user_tools") 
                                                               & (F.action == "select") 
                                                               & (F.object_type=='object_workers')),UserInfo())
async def process_worker_select(callback: CallbackQuery, callback_data: ObjListCallback, user_info: User):
    """Handle worker selection"""
    async with async_session_maker() as session:
        tools = await ToolDAO.find_all(session, ToolFilterModel(user_id=callback_data.id))
        if not tools:
            await callback.answer(get_text("user_has_no_tools", user_info.language))
            return

        xlsx_file = create_user_tools_report(tools, user_info, user_info.language)
        input_file = BufferedInputFile(
            xlsx_file.getvalue(),
            filename=f"tools_{callback_data.id}.xlsx"
        )
        await callback.message.delete()
        await callback.message.answer_document(
            document=input_file,
            caption=get_text(
                "user_tools_list",
                user_info.language,
                full_name=user_info.user_enter_fio
            )
        )
