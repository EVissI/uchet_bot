from aiogram import Router,F
from aiogram.types import Message,CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.exceptions import TelegramBadRequest

from loguru import logger

from app.bot.common.states import AdminNotify
from app.bot.common.texts import get_all_texts,get_text
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import AdminNotifyCallback, ObjListCallback, build_obj_list_kbd, get_admin_notify_kbd
from app.bot.kbds.markup_kbds import MainKeyboard
from app.db.schemas import ObjectFilterModel, UserFilterModel
from app.db.dao import ObjectDAO, ObjectMemberDAO, UserDAO
from app.db.database import async_session_maker
from app.db.models import User

admin_notify_router = Router()


@admin_notify_router.message(F.text.in_(get_all_texts('notify_btn')),UserInfo())
async def process_notify_btn(message:Message, user_info:User):
    await message.delete()
    await message.answer('admin_notify', reply_markup=get_admin_notify_kbd(lang=user_info.language))


@admin_notify_router.callback_query(AdminNotifyCallback.filter(F.type == 'all_users'))
async def process_notify_all_users(callback:CallbackQuery, callback_data:AdminNotifyCallback, state:FSMContext, user_info:User):
    await callback.message.delete()
    await callback.message.answer(get_text('admin_notify_all_user_w8_message',lang=user_info.language))
    await state.set_state(AdminNotify.waiting_message)


@admin_notify_router.message(F.text, StateFilter(AdminNotify.waiting_message),UserInfo())
async def notify_all_users(message:Message,state:FSMContext,user_info:User):
    success_count = 0
    failed_count = 0
    
    async with async_session_maker() as session:
        users = await UserDAO.find_all(session, UserFilterModel())
        if not users:
            await message.answer(
                text=get_text('no_users_found', user_info.language),
                reply_markup=MainKeyboard.build_main_kb(user_info.role, user_info.language)
            )
            await state.clear()
            return

        status_msg = await message.answer(
            text=get_text(
                'sending_notifications_status',
                user_info.language,
                total=len(users),
                sent=0
            )
        )

        for i, user in enumerate(users, 1):
            try:
                await message.bot.send_message(
                    chat_id=user.telegram_id,
                    text=message.text
                )
                success_count += 1
            except TelegramBadRequest as e:
                logger.error(f"Failed to send message to user {user.telegram_id}: {e}")
                failed_count += 1

            if i % 5 == 0:  # Update status every 5 messages
                await status_msg.edit_text(
                    text=get_text(
                        'sending_notifications_status',
                        user_info.language,
                        total=len(users),
                        sent=i
                    )
                )

    await status_msg.edit_text(
        text=get_text(
            'notifications_sent_status',
            user_info.language,
            total=len(users),
            success=success_count,
            failed=failed_count
        )
    )
    await state.clear()


@admin_notify_router.callback_query(AdminNotifyCallback.filter(F.type == "object"), UserInfo())
async def process_notify_object(
    callback: CallbackQuery,
    callback_data: AdminNotifyCallback,
    state: FSMContext,
    user_info: User
):
    """Handle object selection for notification"""
    await callback.message.delete()
    async with async_session_maker() as session:
        objects = await ObjectDAO.find_all(session, filters=ObjectFilterModel(is_active=True))
        if not objects:
            await callback.message.answer(
                text=get_text('no_objects_found', user_info.language),
                reply_markup=MainKeyboard.build_main_kb(user_info.role, user_info.language)
            )
            return
            
        await callback.message.answer(
            text=get_text('select_object_for_notification', user_info.language),
            reply_markup=build_obj_list_kbd(objects, context="notify")
        )


@admin_notify_router.callback_query(ObjListCallback.filter(F.context == "notify", F.action == "select"), UserInfo())
async def process_object_selection(
    callback: CallbackQuery,
    callback_data: ObjListCallback,
    state: FSMContext,
    user_info: User
):
    """Handle selected object and wait for message"""
    await callback.message.delete()
    await state.update_data(selected_object_id=callback_data.id)
    await state.set_state(AdminNotify.waiting_object_message)
    await callback.message.answer(
        text=get_text('enter_notification_text', user_info.language)
    )


@admin_notify_router.message(F.text, StateFilter(AdminNotify.waiting_object_message), UserInfo())
async def notify_object_members(message: Message, state: FSMContext, user_info: User):
    """Send notification to object members"""
    data = await state.get_data()
    object_id = data['selected_object_id']
    success_count = 0
    failed_count = 0
    
    async with async_session_maker() as session:
        members = await ObjectMemberDAO.find_object_members(session, object_id)
        if not members:
            await message.answer(
                text=get_text('no_members_found', user_info.language),
                reply_markup=MainKeyboard.build_main_kb(user_info.role, user_info.language)
            )
            await state.clear()
            return

        status_msg = await message.answer(
            text=get_text(
                'sending_notifications_status',
                user_info.language,
                total=len(members),
                sent=0
            )
        )

        for i, member in enumerate(members, 1):
            try:
                await message.bot.send_message(
                    chat_id=member.telegram_id,
                    text=message.text
                )
                success_count += 1
            except TelegramBadRequest as e:
                logger.error(f"Failed to send message to user {member.telegram_id}: {e}")
                failed_count += 1

            if i % 5 == 0:
                await status_msg.edit_text(
                    text=get_text(
                        'sending_notifications_status',
                        user_info.language,
                        total=len(members),
                        sent=i
                    )
                )

    await status_msg.edit_text(
        text=get_text(
            'notifications_sent_status',
            user_info.language,
            total=len(members),
            success=success_count,
            failed=failed_count
        )
    )
    await state.clear()