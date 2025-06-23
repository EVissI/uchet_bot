from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.bot.common.states import AdminPanelStates, MaterialRemainderStates
from app.bot.common.texts import get_all_texts, get_text
from app.bot.filters.role_filter import RoleFilter
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.markup_kbds import get_back_keyboard,MainKeyboard
from app.db.dao import MaterialReminderDAO
from app.db.models import User
from app.db.database import async_session_maker
from app.db.schemas import MaterialReminderFilter,MaterialReminderModel
from app.config import settings

material_router = Router()
material_router.message.filter(RoleFilter([User.Role.worker.value,
                                          User.Role.foreman.value]))

@material_router.message(
    F.text.in_(get_all_texts("material_remainder_btn")), UserInfo()
)
async def process_material_remainder(message: Message, state: FSMContext, user_info:User):
    await state.set_state(MaterialRemainderStates.waiting_photo)
    await message.answer(
        text=get_text("send_material_photo", user_info.language),reply_markup=get_back_keyboard(user_info.language)
    )

@material_router.message(F.text.in_(get_all_texts("back_btn")), UserInfo())
async def cmd_back(message: Message, state: FSMContext, user_info: User):
    await state.clear()
    await message.answer(
        text=get_text(message.text, user_info.language),
        reply_markup=MainKeyboard.build_main_kb(user_info.role, user_info.language))

@material_router.message(
    F.photo, StateFilter(MaterialRemainderStates.waiting_photo), UserInfo()
)
async def process_material_photo(message: Message, state: FSMContext,user_info:User):
    await state.update_data(photo_id=message.photo[-1].file_id)
    await state.set_state(MaterialRemainderStates.waiting_description)

    await message.answer(
        text=get_text("enter_material_description", user_info.language)
    )


@material_router.message(
    StateFilter(MaterialRemainderStates.waiting_description), UserInfo()
)
async def process_material_description(message: Message, state: FSMContext,user_info:User):
    await state.update_data(description=message.text)
    await state.set_state(MaterialRemainderStates.waiting_location)

    await message.answer(
        text=get_text("enter_storage_location", user_info.language)
    )


@material_router.message(
    StateFilter(MaterialRemainderStates.waiting_location), UserInfo()
)
async def process_material_location(
    message: Message, state: FSMContext, user_info: User
):
    data = await state.get_data()

    material_text = get_text(
        "material_remainder_format",
        user_info.language,
        description=data["description"],
        location=message.text,
    )

    sent_message = await message.bot.send_photo(
        chat_id=settings.TELEGRAM_GROUP_ID_MATERIAL,
        photo=data["photo_id"],
        caption=material_text,
    )

    async with async_session_maker() as session:
        await MaterialReminderDAO.add(
            session,
            MaterialReminderModel(
                file_id=data["photo_id"],
                description=data["description"],
                storage_location=message.text,
                message_id=sent_message.message_id,
                is_active=True
            ),
        )

    await message.answer(text=get_text("material_saved", user_info.language))
    await state.clear()


@material_router.message(
    ~F.photo, StateFilter(MaterialRemainderStates.waiting_photo), UserInfo()
)
async def process_invalid_material_photo(message: Message, user_info: User):
    await message.answer(text=get_text("send_photo_only", user_info.language))

