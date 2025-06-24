from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from app.bot.common.texts import get_text, get_all_texts
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.markup_kbds import MainKeyboard, get_back_keyboard
from app.db.models import User, Tool
from app.db.dao import ToolDAO, UserDAO
from app.db.database import async_session_maker
from app.db.schemas import ToolFilterModel
from app.config import settings
from app.bot.kbds.inline_kbds import (
    ConfirmTransferToolCallback,
    get_accept_tool_keyboard,
    AcceptToolCallback,
    get_confirm_transfer_tool_kbd,
)
from app.bot.common.fsm_managment import DialogMessageManager, StateHistoryMixin


class TransferToolRouter(Router, StateHistoryMixin, DialogMessageManager):
    def __init__(self):
        super().__init__()


transfer_tool_router = TransferToolRouter()

class TransferToolStates(StatesGroup):
    waiting_tool_id = State()
    waiting_user_id = State()
    waiting_confirm = State()


@transfer_tool_router.message(
    F.text.in_(get_all_texts("transfer_tool_btn")), UserInfo()
)
async def transfer_tool_start(message: Message, state: FSMContext, user_info: User):
    await transfer_tool_router.save_message(state, message.message_id)  
    msg = await message.answer(
        get_text("enter_tool_id", user_info.language), reply_markup=get_back_keyboard(user_info.language)
    )
    await transfer_tool_router.save_message(state, msg.message_id)
    await state.set_state(TransferToolStates.waiting_tool_id)


@transfer_tool_router.message(F.text.in_(get_all_texts("back_btn")), 
                            StateFilter(TransferToolStates),
                            UserInfo())
async def transfer_tool_back(message: Message, state: FSMContext, user_info: User):
    await transfer_tool_router.save_message(state, message.message_id)  
    await message.answer(
        message.text,
        reply_markup=MainKeyboard.build_main_kb(user_info.role, user_info.language)
    )
    await transfer_tool_router.clear_messages(state, message.chat.id, message.bot)
    await state.clear()


@transfer_tool_router.message(F.text, 
                            StateFilter(TransferToolStates.waiting_tool_id), 
                            UserInfo())
async def transfer_tool_get_tool_id(
    message: Message, state: FSMContext, user_info: User
):
    await transfer_tool_router.save_message(state, message.message_id)  
    try:
        tool_id = int(message.text.strip())
    except ValueError:
        msg = await message.answer(
            get_text("transfer_tool_invalid_tool_id", user_info.language)
        )
        await transfer_tool_router.save_message(state, msg.message_id)
        return

    async with async_session_maker() as session:
        if user_info.role == User.Role.admin.value or user_info.role == User.Role.buyer.value:
            tool: Tool = await ToolDAO.find_one_or_none(
                session, ToolFilterModel()
            )
        else:
            tool: Tool = await ToolDAO.find_one_or_none(
                session, ToolFilterModel(id=tool_id, user_id=user_info.telegram_id)
            )
        if not tool:
            msg = await message.answer(
                get_text("transfer_tool_not_found", user_info.language)
            )
            await transfer_tool_router.save_message(state, msg.message_id)
            return

    await state.update_data(tool_id=tool_id)
    msg = await message.answer(get_text("enter_recipient", user_info.language))
    await transfer_tool_router.save_message(state, msg.message_id)
    await state.set_state(TransferToolStates.waiting_user_id)


@transfer_tool_router.message(F.text, StateFilter(TransferToolStates.waiting_user_id), UserInfo())
async def transfer_tool_get_user_id(
    message: Message, state: FSMContext, user_info: User
):
    await transfer_tool_router.save_message(state, message.message_id)  
    data = await state.get_data()
    tool_id = data["tool_id"]
    recipient = message.text.strip()

    if recipient.startswith("@"):
        try:
            chat = await message.bot.get_chat(recipient)
            recipient_chat_id = chat.id
        except Exception:
            msg = await message.answer(
                get_text("transfer_tool_recipient_not_found", user_info.language)
            )
            await transfer_tool_router.save_message(state, msg.message_id)
            return
    else:
        try:
            recipient_chat_id = int(recipient)
        except ValueError:
            msg = await message.answer(
                get_text("transfer_tool_invalid_recipient", user_info.language)
            )
            await transfer_tool_router.save_message(state, msg.message_id)
            return

    await state.update_data(recipient_id=recipient_chat_id)
    msg = await message.answer(
        get_text("confirm_transfer_tool", user_info.language),
        reply_markup=get_confirm_transfer_tool_kbd(
            tool_id, recipient_chat_id, user_info.role, lang=user_info.language
        ),
    )
    await transfer_tool_router.save_message(state, msg.message_id)
    await state.set_state(TransferToolStates.waiting_confirm)


@transfer_tool_router.callback_query(ConfirmTransferToolCallback.filter(), UserInfo())
async def process_confirm_transfer_tool(
    callback: CallbackQuery,
    callback_data: ConfirmTransferToolCallback,
    state: FSMContext,
    user_info: User,
):
    tool_id = callback_data.tool_id
    recipient_id = callback_data.recipient_id
    action = callback_data.action
    await callback.message.delete()
    if action == "cancel":
        await callback.message.answer(get_text('operation_cancelled',lang=user_info.language),
                                    reply_markup=MainKeyboard.build_main_kb(user_info.role,user_info.language))

        await transfer_tool_router.clear_messages(
            state, callback.message.chat.id, callback.bot
        )
        await state.clear()
        return

    async with async_session_maker() as session:
        tool: Tool = await ToolDAO.find_one_or_none(
            session, ToolFilterModel(id=tool_id)
        )
        recipient: User = await UserDAO.find_by_telegram_id(session, recipient_id)
        if not tool:
            await callback.message.answer(
                get_text("transfer_tool_not_found", user_info.language),
                reply_markup=MainKeyboard.build_main_kb(user_info.role,user_info.language)
            )
            await transfer_tool_router.clear_messages(
                state, callback.message.chat.id, callback.bot
            )
            await state.clear()
            return

        if action == "force" and user_info.role == User.Role.admin:
            tool.user_id = recipient_id
            await ToolDAO.update(
                session,
                filters=ToolFilterModel(id=tool.id),
                values=ToolFilterModel.model_validate(tool.to_dict()),
            )
            await callback.message.answer(
                get_text("transfer_tool_forced", user_info.language),
                reply_markup=MainKeyboard.build_main_kb(user_info.role,user_info.language)
            )
            await callback.bot.send_message(
                chat_id=recipient_id,
                text=get_text(
                    "transfer_tool_receive_force_prompt",
                    recipient.language,
                    tool_name=tool.name,
                ),
            )
            await transfer_tool_router.clear_messages(
                state, callback.message.chat.id, callback.bot
            )
            await state.clear()
            return

        if action == "confirm":
            transfer_text = get_text(
                "transfer_tool_format",
                user_info.language,
                tool_name=tool.name,
                tool_id=tool_id,
                recipient=recipient_id,
                sender=user_info.user_enter_fio,
            )
            await callback.bot.send_message(
                chat_id=settings.TELEGRAM_GROUP_ID_TRANSFER_TOOL, text=transfer_text
            )
            await callback.bot.send_message(
                chat_id=recipient_id,
                text=get_text(
                    "transfer_tool_receive_prompt",
                    recipient.language,
                    tool_name=tool.name,
                ),
                reply_markup=get_accept_tool_keyboard(tool_id, user_info.language)
            )
            await callback.message.answer(
                get_text("transfer_tool_request_sent", user_info.language),
                reply_markup=MainKeyboard.build_main_kb(user_info.role,user_info.language)
            )
            await transfer_tool_router.clear_messages(
                state, callback.message.chat.id, callback.bot
            )
            await state.clear()


@transfer_tool_router.callback_query(AcceptToolCallback.filter(), UserInfo())
async def accept_tool(
    callback_query: CallbackQuery, callback_data: AcceptToolCallback, user_info: User
) -> None:
    tool_id = callback_data.tool_id
    async with async_session_maker() as session:
        tool: Tool = await ToolDAO.find_one_or_none_by_id(session, tool_id)
        if tool:
            tool.user_id = callback_query.from_user.id
            await ToolDAO.update(
                session,
                filters=ToolFilterModel(id=tool.id),
                values=ToolFilterModel.model_validate(tool.to_dict()),
            )
    await callback_query.message.edit_text(
        get_text("tool_received_confirmation", user_info.language)
    )
