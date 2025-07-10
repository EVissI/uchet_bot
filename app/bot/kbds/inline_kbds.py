from typing import Any, Optional
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.db.models import Object, ObjectDocument, User, ProficAccounting
from app.bot.common.texts import get_text


class LanguageCallback(CallbackData, prefix="lang"):
    lang: str


class CheckUsernameCallback(CallbackData, prefix="check_username"):
    action: str


class ProfileCallback(CallbackData, prefix="profile"):
    action: str


class WorkerObjectActionCallback(CallbackData, prefix="object"):
    action: str
    object_id: int


class AcceptToolCallback(CallbackData, prefix="accept_tool"):
    tool_id: int


class ForemanObjectCallback(CallbackData, prefix="foreman"):
    action: str
    object_id: int


class ForemanBackCallback(CallbackData, prefix="foreman_back"):
    object_id: int


class ForemanOwnExpenseCallback(CallbackData, prefix="foreman_own_expense"):
    flag: bool


class ForemanExpenseTypeCallback(CallbackData, prefix="expense_type"):
    expense_type: str
    object_id: int





class ObjectDocumentTypeCallback(CallbackData, prefix="doc_type"):
    type: str
    document_index: int


class UploadWithoutDocumentsCallback(CallbackData, prefix="upload_without_documents"):
    pass


class AdminNotifyCallback(CallbackData, prefix="admin_notify"):
    type: str


class BulkTransferCallback(CallbackData, prefix="bulk_transfer"):
    action: str


class TMCCallback(CallbackData, prefix="tmc"):
    action: str


def lang_select_kbd(lang: str = "ru") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text=get_text("ru", lang), callback_data=LanguageCallback(lang="ru").pack()
    )
    kb.button(
        text=get_text("uz", lang), callback_data=LanguageCallback(lang="uz").pack()
    )
    kb.button(
        text=get_text("tg", lang), callback_data=LanguageCallback(lang="tg").pack()
    )
    kb.adjust(1)
    return kb.as_markup()


def check_username_kbd(lang: str = "ru") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text=get_text("check", lang=lang),
        callback_data=CheckUsernameCallback(action="check").pack(),
    )
    kb.button(
        text=get_text("create_username", lang=lang),
        callback_data=CheckUsernameCallback(action="create").pack(),
    )
    kb.adjust(1)
    return kb.as_markup()


def profile_keyboard(lang: str = "ru") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text=get_text("tools_list_btn", lang),
        callback_data=ProfileCallback(action="tools").pack(),
    )
    kb.button(
        text=get_text("language_select_btn", lang),
        callback_data=ProfileCallback(action="language").pack(),
    )
    kb.button(
        text=get_text("rules_btn", lang),
        callback_data=ProfileCallback(action="rules").pack(),
    )
    kb.adjust(1)
    return kb.as_markup()


def object_keyboard(object_id: int, lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    buttons = [
        ("docs", "documentation_btn"),
        ("notify", "notify_object_btn"),
        ("photo", "object_photo_btn"),
        ("checks", "object_checks_btn"),
    ]
    kb.button(
        text=get_text("navigation_btn", lang),url="https://www.google.com/search?newwindow=1&sca_esv=c258e1c0eae32aae&sxsrf=AE3TifM8d9GSJVsBLWHTaa6Q3jX9CLPhNg:1750705975247&q=%D0%BA%D0%BE%D1%82%D1%8F%D1%82%D0%B0&udm=2&fbs=AIIjpHyXXa-jR7m04g-bjvdj4k5-Vu3thElMpfRBVcMe0k2JrE5odrMqNgCgijMYA8L8BKYFOPKWasYb6Sc66gofWnAFgtvjmOgtSzH56oaGGp2x7ipLkG6mGLQeI_e1XL-anLGCTnp332Xw4whWM7_EqQkVACciM6dYpfOME3lzEUhxCFYTJX_O8MhoTT-KCYdL4O2C5XMgfX3GYGD6Kc86QKWMYt-fD9JdlCsUKsMCKWSM1mjSF6Qo5GvbxmjNwgxyXr36BBYuXrRUFA60LVywm-_orWFDsg&sa=X&ved=2ahUKEwiQ44r-n4iOAxWHrlYBHcsPKRgQtKgLKAF6BAgTEAE&biw=1920&bih=919&dpr=1"
    )
    for action, text_code in buttons:
        kb.button(
            text=get_text(text_code, lang),
            callback_data=WorkerObjectActionCallback(
                action=action, object_id=object_id
            ).pack(),
        )

    kb.adjust(2, 2, 1)
    return kb.as_markup()


def get_accept_tool_keyboard(tool_id: int, lang: str = "ru") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text=get_text("accept_tool_btn", lang),
        callback_data=AcceptToolCallback(tool_id=tool_id).pack(),
    )
    kb.adjust(1)
    return kb.as_markup()


def get_foreman_objects_kbd(object_id: int, lang: str = "ru") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text=get_text("foreman_workers_btn", lang),
        callback_data=ForemanObjectCallback(
            action="workers", object_id=object_id
        ).pack(),
    )
    kb.button(
        text=get_text("foreman_documentation_btn", lang),
        callback_data=ForemanObjectCallback(
            action="documentation", object_id=object_id
        ).pack(),
    )
    kb.button(
        text=get_text("foreman_photos_btn", lang),
        callback_data=ForemanObjectCallback(
            action="photos", object_id=object_id
        ).pack(),
    )
    kb.button(
        text=get_text("foreman_handover_btn", lang),
        callback_data=ForemanObjectCallback(
            action="handover", object_id=object_id
        ).pack(),
    )
    # kb.button(text=get_text("foreman_procurement_btn", lang), callback_data=ForemanObjectCallback(action="procurement", object_id=object_id).pack())
    kb.button(
        text=get_text("foreman_receipts_btn", lang),
        callback_data=ForemanObjectCallback(
            action="receipts", object_id=object_id
        ).pack(),
    )
    # kb.button(text=get_text("foreman_material_balance_btn", lang), callback_data=ForemanObjectCallback(action="material_balance", object_id=object_id).pack())
    kb.button(
        text=get_text("foreman_info_btn", lang),
        callback_data=ForemanObjectCallback(action="info", object_id=object_id).pack(),
    )
    kb.button(
        text=get_text("foreman_tools_list_btn", lang),
        callback_data=ForemanObjectCallback(
            action="tools_list", object_id=object_id
        ).pack(),
    )
    kb.button(
        text=get_text("foreman_mass_mailing_btn", lang),
        callback_data=ForemanObjectCallback(
            action="mass_mailing", object_id=object_id
        ).pack(),
    )
    # kb.button(text=get_text("foreman_offsite_accounting_btn", lang), callback_data=ForemanObjectCallback(action="offsite_accounting", object_id=object_id).pack())
    kb.button(
        text=get_text("foreman_export_xlsx_btn", lang),
        callback_data=ForemanObjectCallback(
            action="export_xlsx", object_id=object_id
        ).pack(),
    )
    kb.button(
        text=get_text("back_btn", lang),
        callback_data=ForemanObjectCallback(action="back", object_id=object_id).pack(),
    )
    kb.adjust(1)
    return kb.as_markup()


def get_back_kbd(lang: str, object_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text=get_text("back_btn", lang),
        callback_data=ForemanBackCallback(object_id=object_id).pack(),
    )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def get_own_expense_kbd(lang: str, flag: bool = False) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if flag:
        kb.button(
            text=get_text("own_expense_true_btn", lang),
            callback_data=ForemanOwnExpenseCallback(flag=flag).pack(),
        )
    if not flag:
        kb.button(
            text=get_text("own_expense_false_btn", lang),
            callback_data=ForemanOwnExpenseCallback(flag=flag).pack(),
        )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)


def get_expense_type_kbd(lang: str, object_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.button(
        text=get_text("all_expenses_btn", lang),
        callback_data=ForemanExpenseTypeCallback(
            expense_type="all", object_id=object_id
        ).pack(),
    )
    kb.button(
        text=get_text("own_expenses_btn", lang),
        callback_data=ForemanExpenseTypeCallback(
            expense_type="own", object_id=object_id
        ).pack(),
    )
    kb.button(
        text=get_text("company_expenses_btn", lang),
        callback_data=ForemanExpenseTypeCallback(
            expense_type="company", object_id=object_id
        ).pack(),
    )
    kb.button(
        text=get_text("back_btn", lang),
        callback_data=ForemanBackCallback(object_id=object_id).pack(),
    )

    kb.adjust(1)
    return kb.as_markup()

class ForemanToolStatusCallback(CallbackData, prefix="foreman_tool_status"):
    status: str

def get_tool_status_kbd(language: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text=get_text("in_work_tools", language),
        callback_data=ForemanToolStatusCallback(status="in_work").pack(),
    )
    kb.button(
        text=get_text("free_tools", language),
        callback_data=ForemanToolStatusCallback(status="free").pack(),
    )
    kb.button(
        text=get_text("repair_tools", language),
        callback_data=ForemanToolStatusCallback(status="repair").pack(),
    )
    kb.adjust(1)
    return kb.as_markup()


def get_obj_document_type_kbd(
    lang: str, document_index: int
) -> InlineKeyboardMarkup:
    """Get keyboard with document types"""
    kb = InlineKeyboardBuilder()

    for doc_type in ObjectDocument.DocumentType:
        kb.button(
            text=get_text(f"doc_type_{doc_type.value}", lang),
            callback_data=ObjectDocumentTypeCallback(
                type=doc_type.value, document_index=document_index
            ),
        )
    kb.adjust(1)
    return kb.as_markup()


def get_updload_without_documents_kbd(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text=get_text("upload_without_documents_btn", lang),
        callback_data=UploadWithoutDocumentsCallback().pack(),
    )
    kb.adjust(1)
    return kb.as_markup()


def get_admin_notify_kbd(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text=get_text("admin_notify_all_users_inline_btn", lang),
        callback_data=AdminNotifyCallback(type="all_users").pack(),
    )
    kb.button(
        text=get_text("admin_notify_object_inline_btn", lang),
        callback_data=AdminNotifyCallback(type="object").pack(),
    )
    kb.adjust(1)
    return kb.as_markup()


def bulk_transfer_tool_btn(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text=get_text("download_template_btn", lang),
        callback_data=BulkTransferCallback(action="template").pack(),
    )
    kb.button(
        text=get_text("start_transfer_btn", lang),
        callback_data=BulkTransferCallback(action="transfer").pack(),
    )
    kb.adjust(2)
    return kb.as_markup()

class AdminToolStatusCallback(CallbackData, prefix="admin_tool_status"):
    status: str

def get_tools_status_export_kbd(language: str) -> InlineKeyboardMarkup:
    """Get keyboard for tools export by status"""
    kb = InlineKeyboardBuilder()

    kb.button(
        text=get_text("tool_status_all", language),
        callback_data=AdminToolStatusCallback(status="all").pack(),
    )
    kb.button(
        text=get_text("in_work_tools", language),
        callback_data=AdminToolStatusCallback(status="in_work").pack(),
    )
    kb.button(
        text=get_text("free_tools", language),
        callback_data=AdminToolStatusCallback(status="free").pack(),
    )
    kb.button(
        text=get_text("repair_tools", language),
        callback_data=AdminToolStatusCallback(status="repair").pack(),
    )
    kb.adjust(1)
    return kb.as_markup()


def build_tmc_upload_kbd(lang: str) -> InlineKeyboardMarkup:
    """Build keyboard for TMC upload options"""
    kb = InlineKeyboardBuilder()

    kb.button(
        text=get_text("tmc_manual_btn", lang),
        callback_data=TMCCallback(action="manual").pack(),
    )
    kb.button(
        text=get_text("tmc_template_btn", lang),
        callback_data=TMCCallback(action="template").pack(),
    )
    kb.button(
        text=get_text("tmc_upload_btn", lang),
        callback_data=TMCCallback(action="upload").pack(),
    )

    kb.adjust(1)
    return kb.as_markup()


class ObjListCallback(CallbackData, prefix="group_list"):
    id: int
    action: str
    context: str
    page: int = 0
    object_type: str
    sub_info:Any

def build_paginated_list_kbd(
    items: list,
    page: int = 0,
    context: str = None,
    sub_info: None|int = None,
    max_buttons: int = 6,
    text_field: str = "name",
    primary_key_name: str = "id",
    object_type: str = 'object'

) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    start_idx = page * max_buttons
    end_idx = start_idx + max_buttons
    current_items = items[start_idx:end_idx]

    for item in current_items:
        kb.button(
            text=getattr(item, text_field),
            callback_data=ObjListCallback(
                id=getattr(item, primary_key_name), 
                action="select", 
                page=page, 
                context=context, 
                object_type=object_type, 
                sub_info=sub_info
            ).pack(),
        )

    nav_buttons = []
    if len(items) > max_buttons:
        if page > 0:
            nav_buttons.append(
                (
                    "←",
                    ObjListCallback(
                        id=0, 
                        action="prev", 
                        page=page, 
                        context=context, 
                        object_type=object_type, 
                        sub_info=sub_info
                    ).pack(),
                )
            )
        if end_idx < len(items):
            nav_buttons.append(
                (
                    "→",
                    ObjListCallback(
                        id=0, 
                        action="next", 
                        page=page, 
                        context=context, 
                        object_type=object_type, 
                        sub_info=sub_info
                    ).pack(),
                )
            )

        for text, callback in nav_buttons:
            kb.button(text=text, callback_data=callback)

    rows = [1] * len(current_items)
    if nav_buttons:
        rows.append(len(nav_buttons))

    kb.adjust(*rows)
    return kb.as_markup(resize_keyboard=True)

class ItemCardCallback(CallbackData, prefix="item_card"):
    item_id: int
    action: str 
    current_page: int = 1
    total_pages: int 
    keyboard_type: str
    order_type:str
    sub_info: Optional[Any] = None

def build_item_card_kbd(
    item_id: int,
    total_pages: int,
    keyboard_type: str = None,
    current_page: int = 1,
    lang: str = "ru",
    order_type="object",
    sub_info: Optional[Any] = None

) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    nav_row = []
    buttons = []
    if current_page > 1:
        nav_row.append((
            "←",
            ItemCardCallback(
                item_id=0,
                action="prev",
                current_page=current_page - 1,
                total_pages=total_pages,
                keyboard_type=keyboard_type,
                order_type=order_type,
                sub_info=sub_info
            ).pack()
        ))
    
    nav_row.append((
        f"{current_page}/{total_pages}",
        ItemCardCallback(
            item_id=0,
            action="counter",
            current_page=current_page,
            total_pages=total_pages,
            keyboard_type=keyboard_type,
            order_type=order_type,
            sub_info=sub_info
        ).pack()
    ))
    
    if current_page < total_pages:
        nav_row.append((
            "→",
            ItemCardCallback(
                item_id=0,
                action="next",
                current_page=current_page + 1,
                total_pages=total_pages,
                keyboard_type=keyboard_type,
                order_type=order_type,
                sub_info=sub_info
            ).pack()
        ))
    if keyboard_type == 'change_material_riminder':
        buttons.append((
            get_text("change_description_material_reminder_btn", lang),
            ItemCardCallback(
                item_id=item_id,
                action="change_description",
                current_page=current_page,
                total_pages=total_pages,
                keyboard_type=keyboard_type,
                order_type=order_type,
                sub_info=sub_info
            ).pack()
        ))
        buttons.append((
            get_text("change_photo_material_reminder_btn", lang),
            ItemCardCallback(
                item_id=item_id,
                action="change_photo",
                current_page=current_page,
                total_pages=total_pages,
                keyboard_type=keyboard_type,
                order_type=order_type,
                sub_info=sub_info
            ).pack()
        ))
        buttons.append((
            get_text("change_storage_location_material_reminder_btn", lang),
            ItemCardCallback(
                item_id=item_id,
                action="change_location",
                current_page=current_page,
                total_pages=total_pages,
                keyboard_type=keyboard_type,
                order_type=order_type,
                sub_info=sub_info
            ).pack()
        ))
    if keyboard_type == 'material_order_view':
        buttons.append((
            get_text("deactivate_material_order_btn", lang),
            ItemCardCallback(
                item_id=item_id,
                action="deactivate",
                current_page=current_page,
                total_pages=total_pages,
                keyboard_type=keyboard_type,
                order_type=order_type,
                sub_info=sub_info
            ).pack()
        ))
    if keyboard_type == 'deactivate_riminder':
        buttons.append((
            get_text("deactivate_reminder_btn", lang),
            ItemCardCallback(
                item_id=item_id,
                action="deactivate",
                current_page=current_page,
                total_pages=total_pages,
                keyboard_type=keyboard_type,
                order_type=order_type,
                sub_info=sub_info
            ).pack()
        ))
    if keyboard_type == 'tool_view':
        buttons.append((
            get_text("back_btn", lang),
            ItemCardCallback(
                item_id=item_id,
                action="back",
                current_page=current_page,
                total_pages=total_pages,
                keyboard_type=keyboard_type,               
                order_type=order_type,
                sub_info=sub_info
            ).pack()
        ))

    for text, callback in nav_row:
        kb.button(text=text, callback_data=callback)
    for text, callback in buttons:
        kb.button(text=text, callback_data=callback)
    kb.adjust(len(nav_row),1)
    return kb.as_markup()

class DeleteItemConfirmCallback(CallbackData, prefix="delete_item"):
    item_id: int
    action: str

def build_delete_item_confirm_kbd(item_id: int, lang: str = "ru") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text=get_text("yes_btn", lang),
        callback_data=DeleteItemConfirmCallback(item_id=item_id, action="confirm").pack(),
    )
    kb.button(
        text=get_text("no_btn", lang),
        callback_data=DeleteItemConfirmCallback(item_id=item_id, action="cancel").pack(),
    )
    kb.adjust(2)
    return kb.as_markup()

class AccountingTypeCallback(CallbackData, prefix="accounting_type"):
    type: str

def build_accounting_type_kb(lang:str):
    kb = InlineKeyboardBuilder()
    for type in ProficAccounting.PaymentType:
        kb.button(
            text=get_text(f"{type.value.capitalize()}", lang),
            callback_data=AccountingTypeCallback(
                type=type.value
            ),
        )
    kb.adjust(1)
    return kb.as_markup()
    
class FinanceReportTypeCallback(CallbackData, prefix="fin_report"):
    action: str 

class FinanceReportPeriodCallback(CallbackData, prefix="fin_period"):
    action: str 

class FinanceReportObjectCallback(CallbackData, prefix="fin_object"):
    object_id: int
    page: int
    action: str 

def get_finance_report_type_kbd(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text=get_text("report_by_objects_btn", lang),
        callback_data=FinanceReportTypeCallback(action="by_object").pack()
    )
    kb.button(
        text=get_text("report_no_objects_btn", lang),
        callback_data=FinanceReportTypeCallback(action="no_object").pack()
    )
    kb.adjust(1)
    return kb.as_markup()

def get_finance_period_kbd(lang: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text=get_text("this_month_btn", lang),
        callback_data=FinanceReportPeriodCallback(action="month").pack()
    )
    kb.button(
        text=get_text("all_time_btn", lang),
        callback_data=FinanceReportPeriodCallback(action="all_time").pack()
    )
    kb.button(
        text=get_text("custom_period_btn", lang),
        callback_data=FinanceReportPeriodCallback(action="custom").pack()
    )
    kb.button(
        text=get_text("back_btn", lang),
        callback_data=FinanceReportPeriodCallback(action="back").pack()
    )
    kb.adjust(1)
    return kb.as_markup()

def get_finance_objects_kbd(
    objects: list[Object], 
    page: int = 0, 
    items_per_page: int = 5,
    lang: str = "ru"
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    
    start_idx = page * items_per_page
    end_idx = start_idx + items_per_page
    current_objects = objects[start_idx:end_idx]
    
    for obj in current_objects:
        kb.button(
            text=obj.name,
            callback_data=FinanceReportObjectCallback(
                object_id=obj.id,
                page=page,
                action="select"
            ).pack()
        )
    
    nav_buttons = []
    if page > 0:
        nav_buttons.append((
            "←", 
            FinanceReportObjectCallback(object_id=0, page=page-1, action="prev").pack()
        ))
    if end_idx < len(objects):
        nav_buttons.append((
            "→", 
            FinanceReportObjectCallback(object_id=0, page=page+1, action="next").pack()
        ))
    
    kb.button(
        text=get_text("back_btn", lang),
        callback_data=FinanceReportObjectCallback(object_id=0, page=0, action="back").pack()
    )
    
    if nav_buttons:
        for text, callback in nav_buttons:
            kb.button(text=text, callback_data=callback)
            
    kb.adjust(1)  
    return kb.as_markup()

def build_profic_start_kbd(lang):
    kb = InlineKeyboardBuilder()
    kb.button(text=get_text("general_accounting_btn", lang), callback_data="profic_general")
    kb.button(text=get_text("object_accounting_btn", lang), callback_data="profic_object")
    kb.adjust(1)
    return kb.as_markup()

class ConfirmTransferToolCallback(CallbackData, prefix="confirm_transfer_tool"):
    tool_id: int
    recipient_id: int
    action: str 

def get_confirm_transfer_tool_kbd(tool_id: int, recipient_id: int, user_role: str, lang: str = "ru"):
    kb = InlineKeyboardBuilder()
    kb.button(
        text="✅ Подтвердить",
        callback_data=ConfirmTransferToolCallback(tool_id=tool_id, recipient_id=recipient_id, action="confirm").pack()
    )
    kb.button(
        text="❌ Отменить",
        callback_data=ConfirmTransferToolCallback(tool_id=tool_id, recipient_id=recipient_id, action="cancel").pack()
    )
    if user_role == User.Role.admin.value or user_role == User.Role.buyer.value:
        kb.button(
            text="⚡ Принудительно",
            callback_data=ConfirmTransferToolCallback(tool_id=tool_id, recipient_id=recipient_id, action="force").pack()
        )
    kb.adjust(1)
    return kb.as_markup()

def inforamtion_buttons(lang:str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text=get_text("info_block_1",lang),
        callback_data="None"
    )
    kb.button(
        text=get_text("info_block_2",lang),
        callback_data="None"
    )

class ObjectViewCallback(CallbackData, prefix="object_view"):
    action: str
    object_id: int

def get_object_view_kbd(object_id: int, is_active: bool, lang: str = "ru") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    if is_active:
        kb.button(
            text=get_text("object_view_deactivate_btn", lang),
            callback_data=ObjectViewCallback(action="activate_deactivate", object_id=object_id).pack(),
        )
    else:
        kb.button(
            text=get_text("object_view_activate_btn", lang),
            callback_data=ObjectViewCallback(action="activate_deactivate", object_id=object_id).pack(),
        )
    kb.button(
        text=get_text("object_view_workers_btn", lang),
        callback_data=ObjectViewCallback(action="workers", object_id=object_id).pack(),
    )
    kb.button(
        text=get_text("object_view_documents_btn", lang),
        callback_data=ObjectViewCallback(action="documents", object_id=object_id).pack(),
    )
    kb.button(
        text=get_text("back_btn", lang),
        callback_data=ObjectViewCallback(action="back", object_id=object_id).pack(),
    )
    kb.adjust(1)
    return kb.as_markup()

class ObjectWorkersViewCallback(CallbackData, prefix="object_workers_view"):
    role: str
    object_id: int

def get_object_workers_view_kbd(object_id: int, lang: str = "ru") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text=get_text("object_view_foreman_btn", lang),
        callback_data=ObjectWorkersViewCallback(role=User.Role.foreman.value, object_id=object_id).pack(),
    )
    kb.button(
        text=get_text("object_view_worker_btn", lang),
        callback_data=ObjectWorkersViewCallback(role=User.Role.worker.value, object_id=object_id).pack(),
    )
    kb.button(
        text=get_text("back_btn", lang),
        callback_data=ObjectWorkersViewCallback(role="back", object_id=object_id).pack(),
    )
    kb.adjust(1)
    return kb.as_markup()

class MaterialOrderTypeCallback(CallbackData, prefix="material_order_type"):
    type: str
    context: str

def get_material_order_type_select(context, lang: str = "ru") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text=get_text("material_order_type_object_btn", lang),
        callback_data=MaterialOrderTypeCallback(type="object",context=context).pack()
    )
    kb.button(
        text=get_text("material_order_type_general_btn", lang),
        callback_data=MaterialOrderTypeCallback(type="general",context=context).pack()
    )
    kb.adjust(1)
    return kb.as_markup()

class CheckTypeCallback(CallbackData, prefix="check_type"):
    type: str

def get_check_type_select(lang: str = "ru") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text=get_text("check_type_object_btn", lang),
        callback_data=CheckTypeCallback(type="object").pack()
    )
    kb.button(
        text=get_text("check_type_general_btn", lang),
        callback_data=CheckTypeCallback(type="general").pack()
    )
    kb.adjust(1)
    return kb.as_markup()

class CheckOwnExpenseCallback(CallbackData, prefix="check_own_expense"):
    flag: bool
    object_id: int

def get_check_own_expense_kbd(object_id: int, lang: str = "ru") -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(
        text=get_text("check_own_expense_true_btn", lang),
        callback_data=CheckOwnExpenseCallback(flag=True, object_id=object_id).pack(),
    )
    kb.button(
        text=get_text("check_own_expense_false_btn", lang),
        callback_data=CheckOwnExpenseCallback(flag=False, object_id=object_id).pack(),
    )
    kb.adjust(1)
    return kb.as_markup()