from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from loguru import logger

from app.bot.common.states import AdminPanelStates, CheckOutObjectStates
from app.bot.common.texts import get_all_texts, get_text
from app.bot.filters.user_info import UserInfo
from app.db.dao import CheckDAO
from app.db.models import User, Check
from app.db.schemas import CheckModel
from app.db.database import async_session_maker
from app.config import settings



checks_out_object_check_router = Router()


@checks_out_object_check_router.message(
    F.text.in_(get_all_texts("out_object_check_btn")),
    StateFilter(AdminPanelStates.main),
    UserInfo(),
)
async def process_out_object_check_btn(
    message: Message, state: FSMContext, user_info: User
):
    """Handle out-of-object check button"""
    logger.info(f"User {user_info.telegram_id} started out-of-object check process")
    await state.set_state(CheckOutObjectStates.waiting_photo)
    await message.answer(
        text=get_text("send_check_photo_and_description", user_info.language)
    )


@checks_out_object_check_router.message(
    F.photo,F.caption, StateFilter(CheckOutObjectStates.waiting_photo), UserInfo()
)
async def process_check_photo(message: Message, state: FSMContext, user_info: User):
    """Handle check photo with description"""
    logger.info(f"User {user_info.telegram_id} uploaded check photo")

    if not message.caption:
        await message.answer(get_text("check_description_required", user_info.language))
        return

    await state.update_data(
        photo_id=message.photo[-1].file_id, description=message.caption
    )
    await state.set_state(CheckOutObjectStates.waiting_amount)
    await message.answer(get_text("enter_check_amount", user_info.language))


@checks_out_object_check_router.message(
    StateFilter(CheckOutObjectStates.waiting_amount), UserInfo()
)
async def process_check_amount(message: Message, state: FSMContext, user_info: User):
    """Handle check amount input"""
    try:
        amount = float(message.text.replace(",", "."))
        if amount <= 0:
            raise ValueError()

        data = await state.get_data()
        check_text = get_text(
            "out_object_check_format",
            user_info.language,
            worker_name=user_info.user_enter_fio,
            username=f"@{user_info.username}" if user_info.username else "нет username",
            description=data["description"],
            amount=amount,
        )

        # Send to second group
        await message.bot.send_photo(
            chat_id=settings.TELEGRAM_GROUP_ID_CHEKS,
            photo=data["photo_id"],
            caption=check_text,
        )

        async with async_session_maker() as session:
            await CheckDAO.add(
                session,
                CheckModel(
                    file_id=data["photo_id"],
                    description=data["description"],
                    amount=amount,
                    user_id=user_info.telegram_id,
                ),
            )

        logger.info(
            f"User {user_info.telegram_id} completed out-of-object check upload"
        )
        await message.answer(get_text("check_saved", user_info.language))
        await state.clear()

    except ValueError:
        await message.answer(get_text("invalid_amount", user_info.language))
    except Exception as e:
        logger.error(
            f"Error processing check amount from user {user_info.telegram_id}: {e}"
        )
        await message.answer(get_text("check_save_error", user_info.language))
        await state.clear()


@checks_out_object_check_router.message(
    ~F.photo,~F.caption, StateFilter(CheckOutObjectStates.waiting_photo), UserInfo()
)
async def process_invalid_check_photo(message: Message, user_info: User):
    """Handle invalid input in check photo state"""
    await message.answer(get_text("send_photo_only", user_info.language))
