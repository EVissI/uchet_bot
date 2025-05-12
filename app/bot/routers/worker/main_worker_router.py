from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from app.config import settings


main_worker_router = Router()


@main_worker_router.message(F.video_note)
async def handle_circle(message: Message):
    try:
        await message.forward(settings.TELEGRAM_GROUP_VIDEO_OTCHET)
        await message.reply("Отчет принят")
    except Exception as e:
        await message.reply("Произошла ошибка при пересылке сообщения.")