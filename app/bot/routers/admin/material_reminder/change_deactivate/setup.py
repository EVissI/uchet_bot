from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext


from app.bot.common.states import AdminPanelStates
from app.bot.common.texts import get_text, get_all_texts
from app.bot.kbds.inline_kbds import ItemCardCallback,build_item_card_kbd
from app.bot.kbds.markup_kbds import AdminMaterialReminderKeyboard
from app.bot.filters.user_info import UserInfo
from app.db.models import MaterialReminder, User
from app.db.dao import MaterialReminderDAO
from app.db.schemas import MaterialReminderFilter
from app.db.database import async_session_maker
from app.bot.routers.admin.material_reminder.change_deactivate.change import change_reminder_router
from app.bot.routers.admin.material_reminder.change_deactivate.deactivate import delete_reminder_router


setup_activate_deactivate_reminder_router = Router()
setup_activate_deactivate_reminder_router.include_routers(
    change_reminder_router,
    delete_reminder_router
)


@setup_activate_deactivate_reminder_router.message(F.text.in_(get_all_texts('change_deactivate_btn')), 
                                                   StateFilter(AdminPanelStates.material_remainder_control),
                                                   UserInfo())
async def setup_activate_deactivate_reminder(message: Message, state: FSMContext,user_info: User):
    await state.set_state(AdminPanelStates.material_remainder_change_deactivate)
    await message.answer(
        text=message.text,
        reply_markup=AdminMaterialReminderKeyboard.ChangeDeactivateKeyboard.build_change_deactivate_kb(user_info.language)
    )

@setup_activate_deactivate_reminder_router.message(F.text.in_(get_all_texts('back_btn')),
                                                   StateFilter(AdminPanelStates.material_remainder_change_deactivate),
                                                   UserInfo())
async def back_to_reminder_control(message: Message, state: FSMContext, user_info: User):
    await state.set_state(AdminPanelStates.material_remainder_control)
    await message.answer(
        text=message.text,
        reply_markup=AdminMaterialReminderKeyboard.get_material_reminder_control_kb(user_info.language)
    )

@setup_activate_deactivate_reminder_router.callback_query(ItemCardCallback.filter(F.action.in_(['next','prev'])),UserInfo())
async def change_deactivate_reminder_card(
    callback: CallbackQuery, 
    callback_data: ItemCardCallback, 
    state: FSMContext, 
    user_info: User
):
    page:int = callback_data.current_page 
    async with async_session_maker() as session:
        page, total_pages, reminder_id = await MaterialReminderDAO.find_material_reminder_by_page(
            session, 
            page=page
        )
        reminder:MaterialReminder = await MaterialReminderDAO.find_one_or_none(session,MaterialReminderFilter(id=reminder_id))
        await callback.message.delete()
        await callback.message.answer_photo(
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

