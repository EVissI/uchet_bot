from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.bot.filters.user_info import UserInfo
from app.bot.common.texts import get_text
from app.config import settings

report_router = Router()

@report_router.message(Command("report"), UserInfo())
async def send_report(message: Message, user_info) -> None:
    """
    Отправка отчета в группу.
    Пользователь отправляет команду в формате:
      /report <текст отчета>
    (может быть с прикрепленной фотографией), и этот отчет пересылается в группу.
    """
    report_text = message.get_args().strip()
    if not report_text:
        await message.reply(get_text("report_empty_text", user_info.language))
        return

    full_report = get_text(
        "report_format",
        user_info.language,
        sender=user_info.user_enter_fio,
        username=f"@{user_info.username}" if user_info.username else "без username",
        report=report_text
    )

    if message.photo:
        photo_file_id = message.photo[-1].file_id
        await message.bot.send_photo(
            chat_id=settings.TELEGRAM_GROUP_ID_FOREMAN_REPORTS,
            photo=photo_file_id,
            caption=full_report
        )
    else:
        await message.bot.send_message(
            chat_id=settings.TELEGRAM_GROUP_ID_FOREMAN_REPORTS,
            text=full_report
        )

    await message.reply(get_text("report_sent_confirmation", user_info.language))