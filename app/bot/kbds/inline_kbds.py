from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.db.models import Object
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

class AcceptToolCallback(CallbackData, prefix="accept_tool"):
    tool_id: int

class ForemanObjectCallback(CallbackData, prefix='foreman'):
    action: str
    object_id: int

class ObjListCallback(CallbackData, prefix="group_list"):
    id: int
    action: str
    page: int = 0

class ForemanBackCallback(CallbackData, prefix='foreman_back'):
    object_id: int

class ForemanOwnExpenseCallback(CallbackData, prefix='foreman_own_expense'):
    flag: bool

class ForemanExpenseTypeCallback(CallbackData, prefix="expense_type"):
    expense_type: str
    object_id: int

def lang_select_kbd(lang:str = 'ru') -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=get_text('ru',lang), callback_data=LanguageCallback(lang='ru').pack())
    kb.button(text=get_text('az',lang), callback_data=LanguageCallback(lang='az').pack())
    kb.button(text=get_text('tg',lang), callback_data=LanguageCallback(lang='tg').pack())
    kb.adjust(1)
    return kb.as_markup()


def check_username_kbd(lang:str = 'ru') -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=get_text('check',lang=lang), callback_data=CheckUsernameCallback(action='check').pack())
    kb.button(text=get_text('create_username',lang=lang), callback_data=CheckUsernameCallback(action='create').pack())
    kb.adjust(1)
    return kb.as_markup()


def profile_keyboard(lang: str = 'ru') -> InlineKeyboardMarkup:
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


def get_accept_tool_keyboard(tool_id: int, lang: str = "ru") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text=get_text("accept_tool_btn", lang),
        callback_data=AcceptToolCallback(tool_id=tool_id).pack()
    )
    kb.adjust(1)
    return kb.as_markup()


def get_foreman_objects_kbd(object_id: int, lang: str = 'ru') -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=get_text("foreman_workers_btn", lang), callback_data=ForemanObjectCallback(action="workers", object_id=object_id).pack())
    kb.button(text=get_text("foreman_documentation_btn", lang), callback_data=ForemanObjectCallback(action="documentation", object_id=object_id).pack())
    kb.button(text=get_text("foreman_photos_btn", lang), callback_data=ForemanObjectCallback(action="photos", object_id=object_id).pack())
    kb.button(text=get_text("foreman_handover_btn", lang), callback_data=ForemanObjectCallback(action="handover", object_id=object_id).pack())
    # kb.button(text=get_text("foreman_procurement_btn", lang), callback_data=ForemanObjectCallback(action="procurement", object_id=object_id).pack())
    kb.button(text=get_text("foreman_receipts_btn", lang), callback_data=ForemanObjectCallback(action="receipts", object_id=object_id).pack())
    # kb.button(text=get_text("foreman_material_balance_btn", lang), callback_data=ForemanObjectCallback(action="material_balance", object_id=object_id).pack())
    kb.button(text=get_text("foreman_info_btn", lang), callback_data=ForemanObjectCallback(action="info", object_id=object_id).pack())
    kb.button(text=get_text("foreman_tools_list_btn", lang), callback_data=ForemanObjectCallback(action="tools_list", object_id=object_id).pack())
    kb.button(text=get_text("foreman_mass_mailing_btn", lang), callback_data=ForemanObjectCallback(action="mass_mailing", object_id=object_id).pack())
    kb.button(text=get_text("foreman_offsite_accounting_btn", lang), callback_data=ForemanObjectCallback(action="offsite_accounting", object_id=object_id).pack())
    kb.button(text=get_text("foreman_export_xlsx_btn", lang), callback_data=ForemanObjectCallback(action="export_xlsx", object_id=object_id).pack())
    kb.button(text=get_text("back_btn", lang), callback_data=ForemanObjectCallback(action="back", object_id=object_id).pack())
    kb.adjust(1)
    return kb.as_markup()


def build_obj_list_kbd(objects: list[Object],page=0) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    max_buttons = 6 
    start_idx = page * max_buttons
    end_idx = start_idx + max_buttons
    current_objects = objects[start_idx:end_idx]

    for object in current_objects:
        kb.button(
            text=object.name,
            callback_data=ObjListCallback(id=object.id, action='select', page=page).pack()

        )

    nav_buttons = []
    if len(objects) > max_buttons:
        if page > 0:
            nav_buttons.append(("←", ObjListCallback(id=0, action='prev', page=page).pack()))
        if end_idx < len(objects):
            nav_buttons.append(("→", ObjListCallback(id=0, action='next', page=page).pack()))
        
        for text, callback in nav_buttons:
            kb.button(text=text, callback_data=callback)

    rows = [1] * len(current_objects)  
    if nav_buttons:
        rows.append(len(nav_buttons)) 

    kb.adjust(*rows)
    return kb.as_markup(resize_keyboard=True)


def get_back_kbd(lang:str, object_id:int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text=get_text('back_btn', lang), callback_data=ForemanBackCallback(object_id=object_id).pack())
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def get_own_expense_kbd(lang:str, flag:bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if flag:
        kb.button(text=get_text('own_expense_true_btn', lang), callback_data=ForemanOwnExpenseCallback(flag=flag).pack())
    if not flag:
        kb.button(text=get_text('own_expense_false_btn', lang), callback_data=ForemanOwnExpenseCallback(flag=flag).pack())
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def get_expense_type_kbd(lang: str, object_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    kb.button(
        text=get_text("all_expenses_btn", lang),
        callback_data=ForemanExpenseTypeCallback(expense_type="all", object_id=object_id).pack()
    )
    kb.button(
        text=get_text("own_expenses_btn", lang),
        callback_data=ForemanExpenseTypeCallback(expense_type="own", object_id=object_id).pack()
    )
    kb.button(
        text=get_text("company_expenses_btn", lang),
        callback_data=ForemanExpenseTypeCallback(expense_type="company", object_id=object_id).pack()
    )
    kb.button(
        text=get_text("back_btn", lang),
        callback_data=ForemanBackCallback(object_id=object_id).pack()
    )
    
    kb.adjust(1)
    return kb.as_markup()