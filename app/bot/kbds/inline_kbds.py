from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.bot.common.texts import get_text


class LanguageCallback(CallbackData, prefix='lang'):
    lang: str

class CheckUsernameCallback(CallbackData, prefix='check_username'):
    action:str


def lang_select_kbd(lang:str = 'ru') -> InlineKeyboardMarkup:
    """
    Returns an inline keyboard for language selection.
    """
    kb = InlineKeyboardBuilder()
    kb.button(text=get_text('ru',lang), callback_data=LanguageCallback(lang='ru').pack())
    kb.button(text=get_text('az',lang), callback_data=LanguageCallback(lang='az').pack())
    kb.button(text=get_text('tg',lang), callback_data=LanguageCallback(lang='tg').pack())
    kb.adjust(1)
    return kb

def check_username_kbd(lang:str = 'ru') -> InlineKeyboardMarkup:
    """
    Returns an inline keyboard for checking username.
    """
    kb = InlineKeyboardBuilder()
    kb.button(text=get_text('check'), callback_data=CheckUsernameCallback(action='check').pack())
    kb.button(text=get_text('create_username'), callback_data=CheckUsernameCallback(action='create').pack())
    kb.adjust(1)
    return kb