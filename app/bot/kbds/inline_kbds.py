from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.common.texts import get_text


class LanguageCallback(CallbackData, prefix='lang'):
    lang: str

class CheckUsernameCallback(CallbackData, prefix='check_username'):
    action:str

class ProfileCallback(CallbackData, prefix='profile'):
    action: str  

class ObjectActionCallback(CallbackData, prefix='object'):
    action: str 
    object_id: int

def lang_select_kbd(lang:str = 'ru') -> InlineKeyboardMarkup:
    """
    Returns an inline keyboard for language selection.
    """
    kb = InlineKeyboardBuilder()
    kb.button(text=get_text('ru',lang), callback_data=LanguageCallback(lang='ru').pack())
    kb.button(text=get_text('az',lang), callback_data=LanguageCallback(lang='az').pack())
    kb.button(text=get_text('tg',lang), callback_data=LanguageCallback(lang='tg').pack())
    kb.adjust(1)
    return kb.as_markup()


def check_username_kbd(lang:str = 'ru') -> InlineKeyboardMarkup:
    """
    Returns an inline keyboard for checking username.
    """
    kb = InlineKeyboardBuilder()
    kb.button(text=get_text('check'), callback_data=CheckUsernameCallback(action='check').pack())
    kb.button(text=get_text('create_username'), callback_data=CheckUsernameCallback(action='create').pack())
    kb.adjust(1)
    return kb.as_markup()


def profile_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
    """
    Returns an inline keyboard with info buttons:
    - Tools list
    - Language selection
    - Rules
    """
    kb = InlineKeyboardBuilder()
    kb.button(
        text=get_text('tools_list_btn', lang),
        callback_data=ProfileCallback(action='tools').pack()
    )
    kb.button(
        text=get_text('language_select_btn', lang),
        callback_data=ProfileCallback(action='language').pack()
    )
    kb.button(
        text=get_text('rules_btn', lang),
        callback_data=ProfileCallback(action='rules').pack()
    )
    kb.adjust(1)
    return kb.as_markup()


def object_keyboard(object_id: int, lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    buttons = [
        ('navigate', 'navigation_btn'),
        ('docs', 'documentation_btn'),
        ('notify', 'notify_object_btn'),
        ('photo', 'object_photo_btn'),
        ('checks', 'object_checks_btn')
    ]
    
    for action, text_code in buttons:
        kb.button(
            text=get_text(text_code, lang),
            callback_data=ObjectActionCallback(
                action=action,
                object_id=object_id
            ).pack()
        )
    
    kb.adjust(2, 2, 1)
    return kb.as_markup()