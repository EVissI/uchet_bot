from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.bot.common.texts import get_text
from app.db.models import User


def get_share_contact_keyboard(lang: str = 'ru') -> ReplyKeyboardMarkup:
    """
    Returns a keyboard with a button to share contact.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(
                text=get_text('share_contact_btn', lang),
                request_contact=True
            )
        ]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def i_got_acquainted_kbds(lang:str = 'ru') -> ReplyKeyboardMarkup:
    """
    Returns one-time keyboard with a button 'i got acquainted'.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(
                text=get_text('i_got_acquainted_btn', lang),
            )
        ]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def stop_kb(lang:str = 'ru') -> ReplyKeyboardMarkup:
    """
    Returns one-time keyboard with a button 'stop'.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[
            KeyboardButton(
                text=get_text('stop_upload_btn', lang),
            )
        ]],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard


class MainKeyboard:
    __worker_kb_texts_list = ['profile_btn','my_objects_btn', 'material_remainder_btn','material_order_btn', 'info_btn']

    __foreman_kb_texts_list = ['profile_btn','objects_btn', 'material_remainder_btn','material_order_btn', 'reminder_out_btn']

    __admin_kb_texts_list = []

    @staticmethod
    def get_worker_kb_texts(lang: str = 'ru') -> dict:
        """
        Returns dictionary with worker keyboard texts based on language
        """
        return {
            text: get_text(text, lang) 
            for text in MainKeyboard.__worker_kb_texts_list
        }
    
    @staticmethod
    def get_foreman_kb_texts(lang: str = 'ru') -> dict:
        """
        Returns dictionary with worker keyboard texts based on language
        """
        return {
            text: get_text(text, lang) 
            for text in MainKeyboard.__foreman_kb_texts_list
        }
    
    @staticmethod
    def get_admin_kb_texts(lang: str = 'ru') -> dict:
        """
        Returns dictionary with worker keyboard texts based on language
        """
        return {
            text: get_text(text, lang) 
            for text in MainKeyboard.__admin_kb_texts_list
        }
    
    @staticmethod
    def build_main_kb(role:User.Role, lang:str) -> ReplyKeyboardMarkup:
        kb = ReplyKeyboardBuilder()
        match role:
            case User.Role.worker.value:
                for val in MainKeyboard.get_worker_kb_texts(lang).values():
                    kb.button(text=val)
                kb.adjust(1,1,2,1)
                return kb.as_markup(resize_keyboard=True)
            case User.Role.foreman.value:
                for val in MainKeyboard.get_foreman_kb_texts(lang).values():
                    kb.button(text=val)
                kb.adjust(1)
                return kb.as_markup(resize_keyboard=True)
            case User.Role.admin.value:
                for val in MainKeyboard.get_admin_kb_texts(lang).values():
                    kb.button(text=val)
                kb.adjust(1)
                return kb.as_markup(resize_keyboard=True)
            case _: 
                raise ValueError

        


