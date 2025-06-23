from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from app.bot.filters.user_info import UserInfo
from app.db.dao import ToolDAO
from app.db.database import async_session_maker
from app.config import settings
from app.db.models import Tool, User
from app.db.schemas import ToolFilterModel
from app.bot.common.texts import get_text
from app.bot.kbds.inline_kbds import get_accept_tool_keyboard, AcceptToolCallback

transfer_router_cmd = Router()


@transfer_router_cmd.message(Command("transfer_tool"), UserInfo())
async def transfer_tool(message: Message, user_info: User) -> None:
    """
    Передача инструмента.

    Форматы команды:
      /transfer_tool <инструмент_ID> <получатель> <описание>
      /transfer_tool <инструмент_ID> <получатель> -f <описание> (только для админов, принудительная передача)
    """

    args = message.get_args().split()
    if len(args) < 3:
        await message.reply(
            get_text("transfer_tool_invalid_format", user_info.language)
        )
        return

    try:
        tool_id = int(args[0])
    except ValueError:
        await message.reply(
            get_text("transfer_tool_invalid_tool_id", user_info.language)
        )
        return

    recipient = args[1]

    force_transfer = False
    if "-f" in args and user_info.role == User.Role.admin.value:
        force_transfer = True
        args.remove("-f")
        description = " ".join(args[2:])
    else:
        description = " ".join(args[2:])

    async with async_session_maker() as session:
        tool: Tool = await ToolDAO.find_one_or_none_by_id(session, tool_id)
        if not tool:
            await message.reply(get_text("transfer_tool_not_found", user_info.language))
            return

        if force_transfer:
            if recipient.startswith("@"):
                try:
                    chat = await message.bot.get_chat(recipient)
                    recipient_id = chat.id
                except Exception:
                    await message.reply(
                        get_text(
                            "transfer_tool_recipient_not_found", user_info.language
                        )
                    )
                    return
            else:
                try:
                    recipient_id = int(recipient)
                except ValueError:
                    await message.reply(
                        get_text("transfer_tool_invalid_recipient", user_info.language)
                    )
                    return
            tool.user_id = recipient_id
            await ToolDAO.update(
                session,
                filters=ToolFilterModel(id=tool.id),
                values=ToolFilterModel.model_validate(tool.to_dict()),
            )

            transfer_text = get_text(
                "transfer_tool_force_format",
                user_info.language,
                tool_name=tool.name,
                tool_id=tool_id,
                recipient=recipient,
                admin=user_info.user_enter_fio,
                description=description,
            )
            if message.photo:
                await message.bot.send_photo(
                    chat_id=settings.TELEGRAM_GROUP_ID_TRANSFER_TOOL,
                    photo=message.photo[-1].file_id,
                    caption=transfer_text,
                )
            else:
                await message.bot.send_message(
                    chat_id=settings.TELEGRAM_GROUP_ID_TRANSFER_TOOL, text=transfer_text
                )

            await message.reply(
                get_text("transfer_tool_force_complete", user_info.language)
            )
            await message.bot.send_message(
                chat_id=recipient_id,
                text=get_text(
                    "transfer_tool_force_received",
                    user_info.language,
                    tool_name=tool.name,
                    admin=user_info.user_enter_fio,
                ),
            )
            return

        transfer_text = get_text(
            "transfer_tool_format",
            user_info.language,
            tool_name=tool.name,
            tool_id=tool_id,
            recipient=recipient,
            sender=user_info.user_enter_fio,
            description=description,
        )

        if message.photo:
            photo_file_id = message.photo[-1].file_id
            await message.bot.send_photo(
                chat_id=settings.TELEGRAM_GROUP_ID_TRANSFER_TOOL,
                photo=photo_file_id,
                caption=transfer_text,
            )
        else:
            await message.bot.send_message(
                chat_id=settings.TELEGRAM_GROUP_ID_TRANSFER_TOOL, text=transfer_text
            )

        await message.reply(get_text("transfer_tool_request_sent", user_info.language))

        if recipient.startswith("@"):
            try:
                chat = await message.bot.get_chat(recipient)
                recipient_chat_id = chat.id
            except Exception:
                await message.reply(
                    get_text("transfer_tool_recipient_not_found", user_info.language)
                )
                return
        else:
            try:
                recipient_chat_id = int(recipient)
            except ValueError:
                await message.reply(
                    get_text("transfer_tool_invalid_recipient", user_info.language)
                )
                return

        kb = get_accept_tool_keyboard(tool_id, user_info.language)
        await message.bot.send_message(
            chat_id=recipient_chat_id,
            text=get_text(
                "transfer_tool_receive_prompt", user_info.language, tool_name=tool.name
            ),
            reply_markup=kb,
        )


