from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.bot.common.texts import get_text
from app.db.models import User


def get_dialog_keyboard(lang: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=get_text("back_btn", lang))
    kb.button(text=get_text("cancel_btn", lang))
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def get_back_keyboard(lang: str) -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=get_text("back_btn", lang))
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)

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

    __foreman_kb_texts_list = ['profile_btn','objects_btn', 'material_remainder_btn','material_order_btn', 'reminder_out_object_btn']

    __admin_kb_texts_list = ['notify_btn','instrument_control_btn','material_remainder_control_btn','object_control_btn'
                             ,'reminder_out_object_btn','reminder_btn',
                             'finance_report_btn']

    __mini_admin_kb_texts_list = [
        'material_remainder_control_btn','reminder_out_object_btn',
    ]

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
    def get_mini_admin_kb_texts(lang: str = 'ru') -> dict:
        """
        Returns dictionary with worker keyboard texts based on language
        """
        return {
            text: get_text(text, lang) 
            for text in MainKeyboard.__mini_admin_kb_texts_list
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
                kb.adjust(1,3,1)
                return kb.as_markup(resize_keyboard=True)
            case User.Role.buyer.value:
                for val in MainKeyboard.get_mini_admin_kb_texts(lang).values():
                    kb.button(text=val)
                kb.adjust(1)
                return kb.as_markup(resize_keyboard=True)
            case _: 
                raise ValueError

class AdminToolsControlKeyboard:
    __tools_control_texts = ['bulk_transfer_btn' ,'tmc_upload_btn','user_tools_list_btn','tools_export_btn','back_btn']

    @staticmethod
    def get_tools_control_texts(lang: str = 'ru') -> dict:
        return {
            text: get_text(text, lang) 
            for text in AdminToolsControlKeyboard.__tools_control_texts
        }
    
    @staticmethod
    def build_tool_control_kb(lang: str) -> ReplyKeyboardMarkup:
        """
        Builds and returns the tool control keyboard.
        """
        kb = ReplyKeyboardBuilder()
        for val in AdminToolsControlKeyboard.get_tools_control_texts(lang).values():
            kb.button(text=val)
        kb.adjust(4,1)
        return kb.as_markup(resize_keyboard=True)
    

class AdminObjectControlKeyboard:        
    __object_control_texts = ['create_object_btn', 'add_worker_to_object_btn','delete_object_btn','back_btn']

    @staticmethod
    def get_object_control_texts(lang: str = 'ru') -> dict:
        return {
            text: get_text(text, lang) 
            for text in AdminObjectControlKeyboard.__object_control_texts
        }
    
    @staticmethod
    def build_object_control_kb(lang: str) -> ReplyKeyboardMarkup:
        """
        Builds and returns the object control keyboard.
        """
        kb = ReplyKeyboardBuilder()
        for val in AdminObjectControlKeyboard.get_object_control_texts(lang).values():
            kb.button(text=val)
        kb.adjust(3,1)
        return kb.as_markup(resize_keyboard=True)

class AdminMaterialReminderKeyboard:

    __material_reminder_texts = ['create_material_reminder_btn', 'excel_view_btn','change_deactivate_btn','back_btn']

    @staticmethod
    def get_material_reminder_texts(lang: str = 'ru') -> dict:
        return {
            text: get_text(text, lang) 
            for text in AdminMaterialReminderKeyboard.__material_reminder_texts
        }
    
    @staticmethod
    def build_material_reminder_kb(lang: str) -> ReplyKeyboardMarkup:
        """
        Builds and returns the material reminder keyboard.
        """
        kb = ReplyKeyboardBuilder()
        for val in AdminMaterialReminderKeyboard.get_material_reminder_texts(lang).values():
            kb.button(text=val)
        kb.adjust(2)
        return kb.as_markup(resize_keyboard=True)
    
    class ChangeDeactivateKeyboard:
        """
        Keyboard for changing or deactivating material reminders.
        """
        __change_deactivate_texts = ['change_reminder_btn', 'deactivate_reminder_btn', 'back_btn']

        @staticmethod
        def get_change_deactivate_texts(lang: str = 'ru') -> dict:
            return {
                text: get_text(text, lang) 
                for text in AdminMaterialReminderKeyboard.ChangeDeactivateKeyboard.__change_deactivate_texts
            }
        
        @staticmethod
        def build_change_deactivate_kb(lang: str) -> ReplyKeyboardMarkup:
            kb = ReplyKeyboardBuilder()
            for val in AdminMaterialReminderKeyboard.ChangeDeactivateKeyboard.get_change_deactivate_texts(lang).values():
                kb.button(text=val)
            kb.adjust(2)
            return kb.as_markup(resize_keyboard=True)