from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.bot.common.states import HandoverStates
from app.bot.common.texts import get_text
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import ForemanObjectCallback, get_back_kbd, ForemanBackCallback,get_foreman_objects_kbd
from app.db.dao import ObjectDAO
from app.db.models import User
from app.db.database import async_session_maker
from app.db.schemas import ObjectFilterModel
from app.config import settings

handover_router = Router()



@handover_router.callback_query(ForemanObjectCallback.filter(F.action == "handover"), UserInfo())
async def process_handover_btn(
    callback: CallbackQuery,
    callback_data: ForemanObjectCallback,
    state: FSMContext,
    user_info: User
) -> None:
    """
    Обработчик нажатия кнопки "Сдача объекта".
    Запрашивает у пользователя описание сдачи объекта.
    """
    await state.update_data(object_id=callback_data.object_id)
    await state.set_state(HandoverStates.waiting_description)
    await callback.message.delete()
    last_senden_msg = await callback.message.answer(
        text=get_text("enter_handover_description", user_info.language),
        reply_markup=get_back_kbd(user_info.language, callback_data.object_id)
    )
    await state.update_data(last_senden_msg_id=last_senden_msg.message_id)


@handover_router.message(StateFilter(HandoverStates.waiting_description), UserInfo())
async def process_handover_description(
    message: Message,
    state: FSMContext,
    user_info: User
) -> None:
    """
    Обработчик получения описания сдачи объекта.
    Формирует сообщение и отправляет его в группу.
    """
    data = await state.get_data()
    await message.delete()
    await message.bot.delete_message(
        chat_id=message.chat.id,
        message_id=data.get('last_senden_msg_id'),
    )
    object_id = data["object_id"]
    
    async with async_session_maker() as session:
        object = await ObjectDAO.find_one_or_none(session, ObjectFilterModel(id=object_id))
        if not object:
            await message.answer(get_text("object_not_found", user_info.language))
            await state.clear()
            return

    handover_text = get_text(
        "handover_format",
        user_info.language,
        object_name=object.name,
        object_id=object_id,
        foreman_name=user_info.user_enter_fio,
        username=f"@{user_info.username}" if user_info.username else "нет username",
        description=message.text
    )

    await message.bot.send_message(
        chat_id=settings.TELEGRAM_GROUP_ID_FOREMAN_REPORTS,
        text=handover_text
    )

    await message.answer(text=get_text("handover_sent", user_info.language))
    await state.clear()
