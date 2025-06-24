from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from app.bot.common.states import AdminPanelStates, ChangeMaterialRemainderStates
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import ItemCardCallback, build_item_card_kbd
from app.db.models import MaterialReminder, User
from app.db.database import async_session_maker
from app.db.dao import MaterialReminderDAO
from app.db.schemas import MaterialReminderFilter
from app.bot.common.texts import get_text, get_all_texts
from app.config import settings

change_reminder_router = Router()


@change_reminder_router.message(
    F.text.in_(get_all_texts("change_reminder_btn")),
    StateFilter(AdminPanelStates.material_remainder_change_deactivate),
    UserInfo()
)
async def change_reminder(message: Message, user_info: User):
    async with async_session_maker() as session:
        reminders = await MaterialReminderDAO.find_all(session,MaterialReminderFilter())
        if not reminders:
            await message.answer(
                text=get_text("no_material_reminders", user_info.language)
            )
            return
        page, total_pages, reminder_id = (
            await MaterialReminderDAO.find_material_reminder_by_page(session, 1)
        )
        reminder:MaterialReminder = await MaterialReminderDAO.find_one_or_none_by_id(session, reminder_id)
        await message.answer_photo(
            photo=reminder.file_id,
            caption=get_text(
                "choose_reminder", 
                user_info.language,
                description=reminder.description,
                storage_location = reminder.storage_location
            ),
            reply_markup=build_item_card_kbd(
                item_id=reminder_id,
                total_pages=total_pages,
                current_page=page,
                lang=user_info.language,
                keyboard_type="change_material_riminder",
            ),
        )


@change_reminder_router.callback_query(
    ItemCardCallback.filter((F.keyboard_type == "change_material_riminder") & (F.action == "change_description")),
    UserInfo(),
)
async def change_reminder_description(
    callback: Message,
    callback_data: ItemCardCallback,
    state: FSMContext,
    user_info: User,
):
    await callback.message.answer(
        text=get_text("enter_new_description", user_info.language),
    )
    await state.update_data(reminder_id=callback_data.item_id)
    await state.set_state(ChangeMaterialRemainderStates.description)


@change_reminder_router.message(
    F.text, StateFilter(ChangeMaterialRemainderStates.description), UserInfo()
)
async def process_change_reminder_description(
    message: Message, state: FSMContext, user_info: User
):
    data = await state.get_data()
    reminder_id = data.get("reminder_id")

    async with async_session_maker() as session:
        reminder: MaterialReminder = await MaterialReminderDAO.find_one_or_none(
            session, MaterialReminderFilter(id=reminder_id)
        )
        await message.bot.delete_message(
            chat_id=settings.TELEGRAM_GROUP_ID_MATERIAL, message_id=reminder.message_id
        )
        material_text = get_text(
            "material_remainder_format",
            user_info.language,
            description=message.text,
            location=reminder.storage_location,
        )
        bot_message = await message.bot.send_photo(
            chat_id=settings.TELEGRAM_GROUP_ID_MATERIAL,
            photo=reminder.file_id,
            caption=material_text,
        )
        await MaterialReminderDAO.update(
            session,
            MaterialReminderFilter(id=reminder_id),
            MaterialReminderFilter(
                description=message.text, message_id=bot_message.message_id
            ),
        )
        await message.answer(
            text=get_text("reminder_description_updated", user_info.language)
        )

    await state.set_state(AdminPanelStates.material_remainder_change_deactivate)


@change_reminder_router.callback_query(
    ItemCardCallback.filter(
        (F.keyboard_type == "change_material_riminder") & (F.action == "change_photo")
    ),
    UserInfo(),
)
async def change_reminder_photo(
    callback: Message,
    callback_data: ItemCardCallback,
    state: FSMContext,
    user_info: User,
):
    """Handle photo change button click"""
    await callback.message.answer(
        text=get_text("enter_new_photo", user_info.language),
    )
    await state.update_data(reminder_id=callback_data.item_id)
    await state.set_state(ChangeMaterialRemainderStates.file)


@change_reminder_router.message(
    F.photo, StateFilter(ChangeMaterialRemainderStates.file), UserInfo()
)
async def process_change_reminder_photo(
    message: Message, state: FSMContext, user_info: User
):
    """Process new photo for material reminder"""
    data = await state.get_data()
    reminder_id = data.get("reminder_id")

    async with async_session_maker() as session:
        reminder: MaterialReminder = await MaterialReminderDAO.find_one_or_none(
            session, MaterialReminderFilter(id=reminder_id)
        )

        # Delete old message
        await message.bot.delete_message(
            chat_id=settings.TELEGRAM_GROUP_ID_MATERIAL, message_id=reminder.message_id
        )

        # Send new message with updated photo
        material_text = get_text(
            "material_remainder_format",
            user_info.language,
            description=reminder.description,
            location=reminder.storage_location,
        )
        bot_message = await message.bot.send_photo(
            chat_id=settings.TELEGRAM_GROUP_ID_MATERIAL,
            photo=message.photo[-1].file_id,
            caption=material_text,
        )

        # Update in database
        await MaterialReminderDAO.update(
            session,
            MaterialReminderFilter(id=reminder_id),
            MaterialReminderFilter(
                file_id=message.photo[-1].file_id, message_id=bot_message.message_id
            ),
        )


    await message.answer(text=get_text("reminder_photo_updated", user_info.language))
    await state.set_state(AdminPanelStates.material_remainder_change_deactivate)


@change_reminder_router.callback_query(
    ItemCardCallback.filter(
        (F.keyboard_type == "change_material_riminder") & (F.action == "change_location")
    ),
    UserInfo(),
)
async def change_reminder_location(
    callback: Message,
    callback_data: ItemCardCallback,
    state: FSMContext,
    user_info: User,
):
    """Handle location change button click"""
    await callback.message.answer(
        text=get_text("enter_new_location", user_info.language),
    )
    await state.update_data(reminder_id=callback_data.item_id)
    await state.set_state(ChangeMaterialRemainderStates.location)


@change_reminder_router.message(
    F.text, StateFilter(ChangeMaterialRemainderStates.location), UserInfo()
)
async def process_change_reminder_location(
    message: Message, state: FSMContext, user_info: User
):
    """Process new location for material reminder"""
    data = await state.get_data()
    reminder_id = data.get("reminder_id")

    async with async_session_maker() as session:
        reminder: MaterialReminder = await MaterialReminderDAO.find_one_or_none(
            session, MaterialReminderFilter(id=reminder_id)
        )

        # Delete old message
        await message.bot.delete_message(
            chat_id=settings.TELEGRAM_GROUP_ID_MATERIAL, message_id=reminder.message_id
        )

        material_text = get_text(
            "material_remainder_format",
            user_info.language,
            description=reminder.description,
            location=message.text,
        )
        bot_message = await message.bot.send_photo(
            chat_id=settings.TELEGRAM_GROUP_ID_MATERIAL,
            photo=reminder.file_id,
            caption=material_text,
        )

        # Update in database
        await MaterialReminderDAO.update(
            session,
            MaterialReminderFilter(id=reminder_id),
            MaterialReminderFilter(
                storage_location=message.text, message_id=bot_message.message_id
            ),
        )

    await message.answer(text=get_text("reminder_location_updated", user_info.language))
    await state.set_state(AdminPanelStates.material_remainder_change_deactivate)
