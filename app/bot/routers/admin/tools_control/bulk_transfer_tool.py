import io
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from openpyxl import load_workbook
from loguru import logger

from app.bot.common.excel.utils import generate_transfer_template
from app.bot.common.states import AdminPanelStates, BulkTransferStates
from app.bot.common.texts import get_all_texts, get_text
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import BulkTransferCallback, bulk_transfer_tool_btn
from app.db.dao import ToolDAO, UserDAO
from app.db.models import Tool, User
from app.db.schemas import ToolFilterModel, UserFilterModel
from app.db.database import async_session_maker


bulk_transfer_router = Router()


@bulk_transfer_router.message(
    F.text.in_(get_all_texts("bulk_transfer_btn")),
    UserInfo(),
)
async def process_bulk_transfer_btn(
    message: Message, state: FSMContext, user_info: User
):
    logger.info(f"User {user_info.telegram_id} started bulk transfer process")
    await message.answer(
        text=get_text("bulk_transfer_instruction", user_info.language),
        reply_markup=bulk_transfer_tool_btn(user_info.language),
    )


@bulk_transfer_router.callback_query(
    BulkTransferCallback.filter(F.action == "template"), UserInfo()
)
async def process_template_download(callback: CallbackQuery, user_info: User):
    """Handle template download button"""
    logger.info(f"User {user_info.telegram_id} requested transfer template")
    try:
        template = generate_transfer_template(user_info.language)
        await callback.message.answer_document(
            document=BufferedInputFile(
                template.getvalue(), filename="tools_transfer_template.xlsx"
            ),
            caption=get_text("template_instruction", user_info.language),
        )
        logger.debug(f"Template sent to user {user_info.telegram_id}")
        await callback.answer()
    except Exception as e:
        logger.error(
            f"Error generating template for user {user_info.telegram_id}: {str(e)}"
        )
        await callback.answer(
            get_text("template_error", user_info.language), show_alert=True
        )


@bulk_transfer_router.callback_query(
    BulkTransferCallback.filter(F.action == "transfer"), UserInfo()
)
async def process_transfer_start(
    callback: CallbackQuery, state: FSMContext, user_info: User
):
    """Handle transfer start button"""
    logger.info(f"User {user_info.telegram_id} started file upload process")
    try:
        await callback.message.delete()
        await callback.message.answer(
            text=get_text("upload_transfer_file", user_info.language)
        )
        await state.set_state(BulkTransferStates.waiting_file)
        await callback.answer()
        logger.debug(f"State set to waiting_file for user {user_info.telegram_id}")
    except Exception as e:
        logger.error(
            f"Error starting transfer for user {user_info.telegram_id}: {str(e)}"
        )


@bulk_transfer_router.message(
    F.document, StateFilter(BulkTransferStates.waiting_file), UserInfo()
)
async def process_transfer_file(message: Message, state: FSMContext, user_info: User):
    """Process uploaded transfer file"""
    logger.info(f"Processing transfer file from user {user_info.telegram_id}")

    if not message.document.file_name.endswith(".xlsx"):
        logger.warning(
            f"Invalid file format from user {user_info.telegram_id}: {message.document.file_name}"
        )
        await message.reply(get_text("invalid_file_format", user_info.language))
        return

    try:
        file_bytes = await message.bot.download(
            message.document.file_id, destination=io.BytesIO()
        )
        logger.debug(f"File downloaded successfully from user {user_info.telegram_id}")

        wb = load_workbook(filename=file_bytes)
        ws = wb.active

        success_transfers = []
        failed_transfers = []
        tools = []

        logger.debug(f"Processing rows for user {user_info.telegram_id}")
        for row in list(ws.rows)[1:]:
            async with async_session_maker() as session:
                try:
                    tool_id = row[0].value
                    recipient_identifier = row[1].value

                    logger.debug(
                        f"Processing row: tool_id={tool_id}, recipient={recipient_identifier}"
                    )

                    if not all([tool_id, recipient_identifier]):
                        logger.warning(
                            f"Skipping incomplete row: tool_id={tool_id}, recipient={recipient_identifier}"
                        )
                        continue

                    tool: Tool = await ToolDAO.find_one_or_none(
                        session, ToolFilterModel(id=tool_id)
                    )
                    recipient: User = await UserDAO.find_by_identifier(
                        session, recipient_identifier
                    )

                    if not tool:
                        logger.warning(f"Tool not found: ID={tool_id}")
                        failed_transfers.append(
                            f"❌ ID:{tool_id} - Инструмент не найден"
                        )
                        continue

                    if not recipient:
                        logger.warning(f"Recipient not found: {recipient_identifier}")
                        failed_transfers.append(
                            f"❌ ID:{tool_id} → {recipient_identifier} - Получатель не найден"
                        )
                        continue

                    logger.info(
                        f"Transferring tool {tool_id} to user {recipient.telegram_id}"
                    )
                    tool.user_id = recipient.telegram_id
                    tool.status = Tool.Status.in_work.value
                    tools.append(tool)
                    success_transfers.append(
                        f"✅ {tool.name} → {recipient.user_enter_fio}"
                    )
                    logger.debug(
                        f"Successfully transferred tool {tool_id} to {recipient.telegram_id}"
                    )

                except Exception as e:
                    logger.error(f"Error processing row {row[0].row}: {str(e)}")
                    failed_transfers.append(f"❌ Строка {row[0].row}: {str(e)}")
        async with async_session_maker() as session:
            await ToolDAO.bulk_update(
                            session,
                            tools
                    )
        logger.info(
            f"Transfer complete for user {user_info.telegram_id}. "
            f"Success: {len(success_transfers)}, Failed: {len(failed_transfers)}"
        )

        await message.answer(
            get_text(
                "bulk_transfer_report",
                user_info.language,
                success="\n".join(success_transfers) if success_transfers else "нет",
                failed="\n".join(failed_transfers) if failed_transfers else "нет",
            )
        )

    except Exception as e:
        logger.error(
            f"Critical error processing file from user {user_info.telegram_id}: {str(e)}"
        )
        await message.answer(
            get_text("bulk_transfer_error", user_info.language, error=str(e))
        )
    finally:
        await state.clear()
        logger.debug(f"State cleared for user {user_info.telegram_id}")
