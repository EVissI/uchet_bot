from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from loguru import logger

from app.bot.common.states import RegistrationStates
from app.bot.common.texts import get_text
from app.bot.common.utils import generate_math_example
from app.bot.kbds.inline_kbds import (
    LanguageCallback,
    CheckUsernameCallback,
    check_username_kbd,
    lang_select_kbd,
)
from app.bot.kbds.markup_kbds import (
    MainKeyboard,
    get_share_contact_keyboard,
    i_got_acquainted_kbds,
    stop_kb,
)
from app.bot.routers.worker.setup_worker_router import main_worker_router
from app.bot.routers.foreman.setup_foreman_router import main_foreman_router
from app.bot.routers.admin.admin_setup_router import main_admin_router
from app.bot.routers.general_routers.object_list_control_kbd import kbd_obj_list_router
from app.bot.routers.general_routers.profile_router import profile_router
from app.bot.routers.general_routers.material_reminder import material_router
from app.bot.routers.general_routers.material_order import material_order_router
from app.bot.routers.general_routers.transfer_tool_cmd import transfer_router_cmd
from app.bot.routers.general_routers.cheks_out_object import (
    checks_out_object_check_router,
)
from app.bot.routers.general_routers.object_control.setup_object_control import (
    setup_object_control_router,
)
from app.bot.routers.admin.admin_buyer_setup import admin_buyer_setup_router
from app.bot.routers.general_routers.transfer_tool import transfer_tool_router
from app.db.dao import UserDAO, UserDocumentDAO
from app.db.database import async_session_maker
from app.db.models import User
from app.db.schemas import UserModel, UserDocumentModel
from app.config import settings

main_router = Router()
main_router.include_routers(
    main_worker_router,
    main_foreman_router,
    main_admin_router,
    kbd_obj_list_router,
    profile_router,
    material_router,
    material_order_router,
    transfer_router_cmd,
    setup_object_control_router,
    checks_out_object_check_router,
    transfer_tool_router,
    admin_buyer_setup_router
)


@main_router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    async with async_session_maker() as session:
        user: User = await UserDAO.find_by_telegram_id(
            session=session, telegram_id=message.from_user.id
        )
    if not user:
        await message.answer(
            get_text(
                "start",
                lang=message.from_user.language_code,
                name=message.from_user.full_name,
            )
        )
        await message.answer(
            get_text("language_select", lang=message.from_user.language_code),
            reply_markup=lang_select_kbd(),
        )
        await state.set_state(RegistrationStates.language)
        return
    if user:
        await message.answer(
            get_text(
                "start",
                lang=message.from_user.language_code,
                name=message.from_user.full_name,
            ),
            reply_markup=MainKeyboard.build_main_kb(role=user.role, lang=user.language),
        )
        await state.clear()


@main_router.callback_query(
    LanguageCallback.filter(), StateFilter(RegistrationStates.language)
)
async def language_select(
    callback: CallbackQuery, callback_data: LanguageCallback, state: FSMContext
):
    lang = callback_data.lang
    await state.update_data(lang=lang)
    await callback.message.delete()
    if callback.from_user.username:
        await state.set_state(RegistrationStates.phone)
        await callback.message.answer(
            get_text("request_contact", lang=lang),
            reply_markup=get_share_contact_keyboard(lang=lang),
        )
        return
    if not callback.from_user.username:
        await state.set_state(RegistrationStates.username)
        await callback.message.answer(
            get_text("username_instruction", lang=lang),
            reply_markup=check_username_kbd(lang=lang),
        )
        return


@main_router.callback_query(
    CheckUsernameCallback.filter(), StateFilter(RegistrationStates.username)
)
async def username_check(
    callback: CallbackQuery, callback_data: CheckUsernameCallback, state: FSMContext
):
    data = await state.get_data()
    lang = data.get("lang")
    if callback.from_user.username:
        await state.set_state(RegistrationStates.phone)
        await callback.message.answer(
            get_text("request_contact", lang=lang),
            reply_markup=get_share_contact_keyboard(lang=lang),
        )
    if not callback.from_user.username:
        await callback.answer(get_text("has_no_username"), lang=lang)


@main_router.message(F.contact, StateFilter(RegistrationStates.phone))
async def process_contact(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang")
    await state.update_data(phone=message.contact.phone_number)
    await message.answer(get_text("reques_fio", lang=lang))
    await state.set_state(RegistrationStates.fio)


@main_router.message(~F.contact, StateFilter(RegistrationStates.phone))
async def unprocess_contact(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang")
    await message.answer(get_text("its_no_contact", lang=lang))


@main_router.message(F.text, StateFilter(RegistrationStates.fio))
async def process_contact(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang")
    await state.update_data(fio=message.text)
    await message.answer(get_text("reques_docs", lang=lang), reply_markup=stop_kb(lang))
    await state.set_state(RegistrationStates.documents)


@main_router.message(F.photo, StateFilter(RegistrationStates.documents))
async def process_photos(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang")
    photos = data.get("photos", [])
    photo_file_id = message.photo[-1].file_id
    photos.append(photo_file_id)
    await state.update_data(photos=photos)
    await message.answer(get_text("photo_received", lang=lang, count=len(photos)))


@main_router.message(
    lambda message: message.text
    in [
        get_text("stop_upload_btn", "ru"),
        get_text("stop_upload_btn", "az"),
        get_text("stop_upload_btn", "tg"),
    ],
    StateFilter(RegistrationStates.documents),
)
async def finish_photos(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang")
    photos = data.get("photos", [])
    if not photos:
        await message.answer(get_text("no_photos", lang=lang))
        return
    await message.answer(get_text("photos_saved", lang=lang, count=len(photos)))
    await message.answer(get_text("instructions", lang=lang))
    await message.answer(get_text("rules", lang=lang))
    await message.answer(
        get_text("i_got_acquainted", lang=lang),
        reply_markup=i_got_acquainted_kbds(lang=lang),
    )
    await state.set_state(RegistrationStates.instructions)


@main_router.message(
    lambda message: message.text
    in [
        get_text("i_got_acquainted_btn", "ru"),
        get_text("i_got_acquainted_btn", "az"),
        get_text("i_got_acquainted_btn", "tg"),
    ],
    StateFilter(RegistrationStates.instructions),
)
async def i_got_acquainted(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang")

    example, answer = generate_math_example()
    await state.update_data(correct_answer=answer)
    await message.answer(get_text("solve_example", lang=lang, example=example))
    await state.set_state(RegistrationStates.verification)


@main_router.message(F.text, RegistrationStates.verification)
async def verify_answer(message: Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("lang")
    correct_answer = data.get("correct_answer")
    documents = data.get("photos")
    try:
        user_answer = int(message.text)
        if user_answer == correct_answer:
            async with async_session_maker() as session:
                new_user = UserModel(
                    telegram_id=message.from_user.id,
                    username=message.from_user.username,
                    language=lang,
                    user_enter_fio=data.get("fio"),
                    phone_number=data.get("phone"),
                    role=User.Role.worker,
                    can_use_bot=True,
                )
                await UserDAO.add(session, new_user)
                for document in documents:
                    await UserDocumentDAO.add(
                        session,
                        UserDocumentModel(
                            file_id=document, user_id=message.from_user.id
                        ),
                    )
            await message.answer(
                get_text("verification_success", lang=lang),
                reply_markup=MainKeyboard.build_main_kb(
                    role=new_user.role, lang=new_user.language
                ),
            )
            await state.clear()
        else:
            example, answer = generate_math_example()
            await state.update_data(correct_answer=answer)
            await message.answer(get_text("wrong_answer", lang=lang, example=example))
    except ValueError as e:
        logger.error(f"{e}")
        await message.answer(get_text("not_a_number", lang=lang))


@main_router.message(Command("chatid"), F.chat.type.in_({"group", "supergroup"}))
async def get_chat_id(message: Message):
    """Returns current chat ID when called from a group"""
    chat_info = await message.bot.get_chat(message.chat.id)
    text = (
        f"📢 Информация о чате:\n\n"
        f"👥 Название: {chat_info.title}\n"
        f"🆔 ID: {chat_info.id}"
    )

    await message.answer(
        text=text,
    )
