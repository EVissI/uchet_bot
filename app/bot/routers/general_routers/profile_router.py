from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from app.bot.common.texts import get_all_texts, get_text
from app.bot.common.utils import escape_markdown
from app.bot.filters.user_info import UserInfo
from app.bot.kbds.inline_kbds import (
    ProfileCallback,
    LanguageCallback,
    lang_select_kbd,
    profile_keyboard,
)
from app.bot.kbds.markup_kbds import MainKeyboard
from app.db.models import User
from app.db.dao import ToolDAO, UserDAO
from app.db.schemas import ToolFilterModel, UserFilterModel
from app.db.database import async_session_maker

profile_router = Router()


@profile_router.message(F.text.in_(get_all_texts("profile_btn")), UserInfo())
async def process_profile_callback(message: Message, user_info: User):
    profile_text = get_text(
        "profile_info",
        lang=user_info.language,
        telegram_id=user_info.telegram_id,
        username=escape_markdown(user_info.username),
        full_name=escape_markdown(user_info.user_enter_fio),
        phone=escape_markdown(user_info.phone_number),
        role=escape_markdown(user_info.role),
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

        await callback.message.answer(
            text=get_text("tools_list_header", lang=user_info.language),
        )

        for tool in tools:
            tool_text = get_text(
                "tool_item",
                lang=user_info.language,
                name=tool.name,
                description=tool.description
                or get_text("no_description", user_info.language),
            )

            if tool.file_id:
                await callback.message.answer_photo(
                    photo=tool.file_id, caption=tool_text
                )
            else:
                await callback.message.answer(text=tool_text)


@profile_router.callback_query(
    ProfileCallback.filter(F.action == "language"), UserInfo()
)
async def process_change_lang_btn(callback: CallbackQuery, user_info: User):
    await callback.message.answer(
        get_text("language_select"),
        reply_markup=lang_select_kbd(lang=user_info.language),
    )


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
    await callback.message.answer(get_text("rules", lang=user_info.language))
