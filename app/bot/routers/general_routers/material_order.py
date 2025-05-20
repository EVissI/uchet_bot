from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from datetime import datetime

from app.bot.common.states import MaterialOrderStates
from app.bot.common.texts import get_all_texts, get_text
from app.bot.filters.user_info import UserInfo
from app.db.dao import MaterialOrderDAO
from app.db.models import User
from app.db.database import async_session_maker
from app.db.schemas import MaterialOrderModel, MaterialOrderFilter
from app.config import settings

material_order_router = Router()


@material_order_router.message(
    F.text.in_(get_all_texts("material_order_btn")), UserInfo()
)
async def process_material_order(message: Message, state: FSMContext, user_info: User):
    """Handler for starting material order process"""
    await state.set_state(MaterialOrderStates.waiting_description)
    await message.answer(text=get_text("enter_material_order", user_info.language))


@material_order_router.message(
    F.text,
    StateFilter(MaterialOrderStates.waiting_description), 
    UserInfo()
)
async def process_order_description(
    message: Message, state: FSMContext, user_info: User
):
    """Handler for receiving material description"""
    await state.update_data(description=message.text)
    await state.set_state(MaterialOrderStates.waiting_date)
    await message.answer(text=get_text("enter_delivery_date", user_info.language))


@material_order_router.message(
    StateFilter(MaterialOrderStates.waiting_date),
    F.text.regexp(r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(20\d{2})$"),
    UserInfo(),
)
async def process_valid_date(message: Message, state: FSMContext, user_info: User):
    """Handler for processing valid date format"""
    try:
        day, month, year = map(int, message.text.split("."))
        input_date = datetime(year, month, day)
        if input_date < datetime.now():
            await message.answer(
                text=get_text("date_must_be_future", user_info.language)
            )
            return
    except ValueError:
        await message.answer(text=get_text("invalid_date", user_info.language))
        return

    data = await state.get_data()
    order_text = get_text(
        "material_order_format",
        user_info.language,
        worker_name=user_info.user_enter_fio,
        username=f"@{user_info.username}" if user_info.username else "нет username",
        description=data["description"],
        delivery_date=message.text,
    )

    sent_message = await message.bot.send_message(
        chat_id=settings.TELEGRAM_GROUP_ID_MATERIAL_ORDER,
        text=order_text,
    )

    async with async_session_maker() as session:
        await MaterialOrderDAO.add(
            session,
            MaterialOrderModel(
                description=data["description"],
                delivery_date=message.text,
                message_id=sent_message.message_id,
            ),
        )

    await message.answer(text=get_text("order_saved", user_info.language))
    await state.clear()


@material_order_router.message(
    StateFilter(MaterialOrderStates.waiting_date),
    ~F.text.regexp(r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(20\d{2})$"),
    UserInfo(),
)
async def process_invalid_date_format(message: Message, user_info: User):
    """Handler for invalid date format"""
    await message.answer(text=get_text("invalid_date_format", user_info.language))
