import random
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from app.bot.filters.user_info import UserInfo
from app.db.dao import ToolDAO, MaterialDAO
from app.db.database import async_session_maker
from app.db.schemas import ToolModel, MaterialModel
from app.config import settings
from app.db.models import User, Tool

admin_tool_material_router = Router()

SAMPLE_TOOLS = [
    ("Дрель", "Аккумуляторная дрель Makita"),
    ("Перфоратор", "Перфоратор Bosch GBH 2-26"),
    ("Болгарка", "УШМ Metabo WE 15-125"),
    ("Шуруповерт", "Шуруповерт DeWalt DCD791"),
    ("Лобзик", "Электролобзик Festool PS 420"),
]

SAMPLE_MATERIALS = [
    ("Цемент", "Цемент М500, 50 кг"),
    ("Песок", "Строительный песок, мелкий"),
    ("Арматура", "Арматура А500С, д.12мм"),
    ("Кирпич", "Кирпич керамический полнотелый"),
    ("Брус", "Брус строительный 150х150"),
]


@admin_tool_material_router.message(Command("create_mock_tools"), UserInfo())
async def create_mock_tools(message: Message, user_info: User) -> None:
    """Создать тестовые записи для инструментов."""
    if message.from_user.id not in settings.ROOT_ADMIN_IDS:
        return

    async with async_session_maker() as session:
        for name, description in SAMPLE_TOOLS:
            tool = ToolModel(
                name=name,
                description=description,
                file_id=None,
                status=random.choice(list(Tool.Status)).value,
                user_id=random.choice(settings.ROOT_ADMIN_IDS),
            )
            await ToolDAO.add(session, tool)

        await message.answer("Тестовые инструменты успешно созданы")


@admin_tool_material_router.message(Command("create_mock_materials"), UserInfo())
async def create_mock_materials(message: Message, user_info: User) -> None:
    """Создать тестовые записи для материалов."""
    if message.from_user.id not in settings.ROOT_ADMIN_IDS:
        return

    async with async_session_maker() as session:
        for name, description in SAMPLE_MATERIALS:
            material = MaterialModel(
                file_id=f"mock_file_{random.randint(1000, 9999)}",
                description=description,
                storage_location=f"Склад {random.randint(1, 5)}",
                message_id=random.randint(1000, 9999),
            )
            await MaterialDAO.add(session, material)

        await message.answer("Тестовые материалы успешно созданы")


@admin_tool_material_router.message(Command("clear_mock_data"), UserInfo())
async def clear_mock_data(message: Message, user_info: User) -> None:
    """Удалить все тестовые данные."""
    if message.from_user.id not in settings.ROOT_ADMIN_IDS:
        return

    async with async_session_maker() as session:
        await ToolDAO.delete_all(session)
        await MaterialDAO.delete_all(session)
        await message.answer("Все тестовые данные удалены")
