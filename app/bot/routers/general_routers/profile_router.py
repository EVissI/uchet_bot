from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.filters import Command

from app.bot.common.texts import get_all_texts, get_text
from app.bot.filters.role_filter import RoleFilter
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import (
    ItemCardCallback,
    ProfileCallback,
    LanguageCallback,
    build_item_card_kbd,
    lang_select_kbd,
    profile_keyboard,
)
from app.bot.kbds.markup_kbds import MainKeyboard
from app.db.models import User
from app.db.dao import ToolDAO, UserDAO
from app.db.schemas import ToolFilterModel, UserFilterModel
from app.db.database import async_session_maker

profile_router = Router()
profile_router.message.filter(RoleFilter([User.Role.worker.value,
                                          User.Role.foreman.value]))


@profile_router.message(F.text.in_(get_all_texts("profile_btn")), UserInfo())
async def process_profile_callback(message: Message, user_info: User):
    profile_text = get_text(
        "profile_info",
        lang=user_info.language,
        telegram_id=user_info.telegram_id,
        username=user_info.username,
        full_name=user_info.user_enter_fio,
        phone=user_info.phone_number,
        role=user_info.role,
    )
    await message.answer(
        text=profile_text,
        reply_markup=profile_keyboard(lang=user_info.language),
    )


@profile_router.callback_query(ProfileCallback.filter(F.action == "tools"), UserInfo())
async def process_tools_btn(callback: CallbackQuery, user_info: User):
    async with async_session_maker() as session:
        tools = await ToolDAO.find_all(
            session, ToolFilterModel(user_id=user_info.telegram_id)
        )

        if not tools:
            await callback.message.answer(get_text("no_tools", lang=user_info.language))
            return
        await callback.message.delete()
        current_tool = tools[0]
        total_pages = len(tools)

        # Format tool card text
        tool_text = get_text(
            "tool_item",
            lang=user_info.language,
            tool_id=current_tool.id,
            name=current_tool.name,
            description=current_tool.description
            or get_text("no_description", user_info.language),
        )

        # Send tool card with navigation keyboard
        if current_tool.file_id:
            await callback.message.answer_photo(
                photo=current_tool.file_id,
                caption=tool_text,
                reply_markup=build_item_card_kbd(
                    item_id=current_tool.id,
                    total_pages=total_pages,
                    keyboard_type="tool_view",
                    current_page=1,
                    lang=user_info.language,
                ),
            )
        else:
            await callback.message.answer(
                text=tool_text,
                reply_markup=build_item_card_kbd(
                    item_id=current_tool.id,
                    total_pages=total_pages,
                    keyboard_type="tool_view",
                    current_page=1,
                    lang=user_info.language,
                ),
            )
        await callback.answer()


@profile_router.callback_query(
    ItemCardCallback.filter(F.keyboard_type == "tool_view"), UserInfo()
)
async def process_tool_navigation(
    callback: CallbackQuery, callback_data: ItemCardCallback, user_info: User
):
    """Handle tool card navigation"""

    if callback_data.action == "back":
        await callback.message.delete()
        await callback.message.answer(
            text=get_text(
                "profile_info",
                lang=user_info.language,
                telegram_id=user_info.telegram_id,
                username=user_info.username,
                full_name=user_info.user_enter_fio,
                phone=user_info.phone_number,
                role=user_info.role,
            ),
            reply_markup=profile_keyboard(user_info.language)
        )
        return
    if callback_data.action in ["prev", "next"]:
        async with async_session_maker() as session:
            tools = await ToolDAO.find_all(
                session, ToolFilterModel(user_id=user_info.telegram_id)
            )

            current_tool = tools[callback_data.current_page - 1]
            tool_text = get_text(
                "tool_item",
                lang=user_info.language,
                tool_id=current_tool.id,
                name=current_tool.name,
                description=current_tool.description
                or get_text("no_description", user_info.language),
            )

            if current_tool.file_id:
                await callback.message.edit_media(
                    media=InputMediaPhoto(
                        media=current_tool.file_id, caption=tool_text
                    ),
                    reply_markup=build_item_card_kbd(
                        item_id=current_tool.id,
                        total_pages=len(tools),
                        keyboard_type="tool_view",
                        current_page=callback_data.current_page,
                        lang=user_info.language,
                    ),
                )
            else:
                await callback.message.edit_text(
                    text=tool_text,
                    reply_markup=build_item_card_kbd(
                        item_id=current_tool.id,
                        total_pages=len(tools),
                        keyboard_type="tool_view",
                        current_page=callback_data.current_page,
                        lang=user_info.language,
                    ),
                )

    await callback.answer()


@profile_router.callback_query(
    ProfileCallback.filter(F.action == "language"), UserInfo()
)
async def process_change_lang_btn(callback: CallbackQuery, user_info: User):
    await callback.message.delete()
    await callback.message.answer(
        get_text("language_select"),
        reply_markup=lang_select_kbd(lang=user_info.language),
    )
    await callback.answer()


@profile_router.callback_query(LanguageCallback.filter(), UserInfo())
async def process_change_lang_inline(
    callback: CallbackQuery, callback_data: LanguageCallback, user_info: User
):
    await callback.message.delete()
    async with async_session_maker() as session:
        user_info.language = callback_data.lang
        await UserDAO.update(
            session,
            filters=UserFilterModel(telegram_id=user_info.telegram_id),
            values=UserFilterModel.model_validate(user_info.to_dict()),
        )
    await callback.message.answer(
        get_text("lang_has_changed"),
        reply_markup=MainKeyboard.build_main_kb(
            role=user_info.role, lang=user_info.language
        ),
    )


@profile_router.callback_query(ProfileCallback.filter(F.action == "rules"), UserInfo())
async def process_rule_btn(callback: CallbackQuery, user_info: User):
    await callback.answer()
    await callback.message.answer(get_text("rules", lang=user_info.language))
