from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter

from app.bot.filters.role_filter import RoleFilter
from app.bot.routers.worker.my_object_router import my_object_router
from app.bot.routers.worker.object_logic.main_object_router import main_worker_object_router
from app.config import settings
from app.db.models import User


main_worker_router = Router()
main_worker_router.message.filter(RoleFilter(User.Role.worker.value))
main_worker_router.include_routers(my_object_router,
                                   main_worker_object_router)

@main_worker_router.message(F.video_note,StateFilter(None))
async def handle_circle(message: Message):
    try:
        await message.forward(settings.TELEGRAM_GROUP_ID_VIDEO_OTCHET)
        await message.reply("Отчет принят")
    except Exception as e:
        await message.reply("Произошла ошибка при пересылке сообщения.")