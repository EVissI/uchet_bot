from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from app.bot.filters.role_filter import RoleFilter
from app.config import settings
from app.db.models import User


main_worker_router = Router()
main_worker_router.message.filter(RoleFilter(User.Role.worker))


@main_worker_router.message(F.video_note)
async def handle_circle(message: Message):
    try:
        await message.forward(settings.TELEGRAM_GROUP_ID_VIDEO_OTCHET)
        await message.reply("Отчет принят")
    except Exception as e:
        await message.reply("Произошла ошибка при пересылке сообщения.")