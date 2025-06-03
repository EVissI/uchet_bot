import io
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from datetime import datetime

from app.bot.common.texts import get_text
from app.db.models import ObjectCheck, Tool, User


def create_expense_report(expenses: list[ObjectCheck], lang: str) -> io.BytesIO:
    """
    Creates an Excel report from expenses list.
    
    Args:
        expenses: List of ObjectCheck instances
        lang: Language code for translations
    
    Returns:
        io.BytesIO: Excel file as bytes buffer
    """
    wb = Workbook()
    ws = wb.active
    ws.title = get_text("expense_sheet_name", lang)

    # Styling
    header_font = Font(bold=True)
    header_fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
    center_align = Alignment(horizontal='center')

    # Headers
    headers = [
        'ID',
        get_text("date_column", lang),
        get_text("description_column", lang),
        get_text("amount_column", lang),
        get_text("expense_type_column", lang),
        get_text("user_column", lang)
    ]

    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align

    # Data
    total_amount = 0
    for row, expense in enumerate(expenses, 2):
        ws.cell(row=row, column=1, value=expense.id)
        ws.cell(row=row, column=2, value=expense.created_at.strftime("%d.%m.%Y"))
        ws.cell(row=row, column=3, value=expense.description)
        ws.cell(row=row, column=4, value=expense.amount)
        ws.cell(row=row, column=5, value=get_text("own_expense", lang) if expense.own_expense else get_text("company_expense", lang))
        ws.cell(row=row, column=6, value=expense.user.user_enter_fio)
        
        total_amount += expense.amount

    # Total row
    total_row = len(expenses) + 2
    ws.cell(row=total_row, column=3, value=get_text("total_amount", lang))
    total_cell = ws.cell(row=total_row, column=4, value=total_amount)
    total_cell.font = Font(bold=True)

    # Column widths
    ws.column_dimensions['A'].width = 10  # ID
    ws.column_dimensions['B'].width = 15  # Date
    ws.column_dimensions['C'].width = 40  # Description
    ws.column_dimensions['D'].width = 15  # Amount
    ws.column_dimensions['E'].width = 20  # Expense type
    ws.column_dimensions['F'].width = 30  # User

    # Save to buffer
    excel_buffer = io.BytesIO()
    wb.save(excel_buffer)
    excel_buffer.seek(0)

    return excel_buffer

def create_tools_report(tools: list[Tool], lang: str) -> io.BytesIO:
    """Create Excel report for tools list"""
    wb = Workbook()
    ws = wb.active
    ws.title = get_text("excel_tools_sheet_name", lang)

    # Styling
    header_font = Font(bold=True)
    header_fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
    center_align = Alignment(horizontal='center')

    # Headers
    headers = [
        get_text("excel_tool_name", lang),
        get_text("excel_tool_description", lang),
        get_text("excel_tool_status", lang),
        get_text("excel_tool_user", lang),
        get_text("excel_tool_date", lang)
    ]

    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align

    # Data
    for row, tool in enumerate(tools, 2):
        ws.cell(row=row, column=1, value=tool.name)
        ws.cell(row=row, column=2, value=tool.description)
        ws.cell(row=row, column=3, value=tool.status)
        ws.cell(row=row, column=4, value=tool.user.user_enter_fio if tool.user else "-")
        ws.cell(row=row, column=5, value=tool.created_at.strftime("%d.%m.%Y"))

    # Column widths
    ws.column_dimensions['A'].width = 30  # Name
    ws.column_dimensions['B'].width = 40  # Description
    ws.column_dimensions['C'].width = 20  # Status
    ws.column_dimensions['D'].width = 30  # User
    ws.column_dimensions['E'].width = 15  # Date

    excel_buffer = io.BytesIO()
    wb.save(excel_buffer)
    excel_buffer.seek(0)

    return excel_buffer

async def create_user_tools_report(tools: list[Tool], user: User, lang: str) -> io.BytesIO:
    """
    Формирует Excel-файл со списком инструментов пользователя.
    :param tools: список инструментов (Tool)
    :param user: объект пользователя (User)
    :param lang: язык для переводов
    :return: io.BytesIO с Excel-файлом
    """
    wb = Workbook()
    ws = wb.active
    ws.title = f"Инструменты {user.user_enter_fio}"

    # Стили
    header_font = Font(bold=True)
    header_fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
    center_align = Alignment(horizontal='center')

    # Заголовки
    headers = [
        get_text("excel_tool_name", lang),
        get_text("excel_tool_description", lang),
        get_text("excel_tool_status", lang),
        get_text("excel_tool_date", lang)
    ]

    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align

    # Данные
    for row, tool in enumerate(tools, 2):
        ws.cell(row=row, column=1, value=tool.name)
        ws.cell(row=row, column=2, value=tool.description)
        ws.cell(row=row, column=3, value=tool.status)
        ws.cell(row=row, column=4, value=tool.created_at.strftime("%d.%m.%Y") if hasattr(tool, "created_at") and tool.created_at else "")

    # Ширина колонок
    ws.column_dimensions['A'].width = 30  # Name
    ws.column_dimensions['B'].width = 40  # Description
    ws.column_dimensions['C'].width = 20  # Status
    ws.column_dimensions['D'].width = 15  # Date

    excel_buffer = io.BytesIO()
    wb.save(excel_buffer)
    excel_buffer.seek(0)
    return excel_buffer

def generate_transfer_template(lang: str) -> io.BytesIO:
    """
    Generate Excel template for bulk tools transfer
    
    Args:
        lang: Language code for translations
    
    Returns:
        io.BytesIO: Excel template file as bytes buffer
    """
    wb = Workbook()
    ws = wb.active
    ws.title = get_text("transfer_template_sheet", lang)

    # Styling
    header_font = Font(bold=True)
    header_fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
    center_align = Alignment(horizontal='center')

    # Headers
    headers = [
        get_text("excel_tool_id", lang),
        get_text("excel_recipient_username", lang),
        get_text("excel_transfer_description", lang)
    ]

    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align

    # Example row
    example_row = [
        "12345",
        "@username",
        "Передача инструмента"
    ]
    for col, value in enumerate(example_row, 1):
        cell = ws.cell(row=2, column=col)
        cell.value = value
        cell.font = Font(italic=True, color="808080")

    # Column widths
    ws.column_dimensions['A'].width = 15  # Tool ID
    ws.column_dimensions['B'].width = 25  # Recipient username
    ws.column_dimensions['C'].width = 40  # Description

    excel_buffer = io.BytesIO()
    wb.save(excel_buffer)
    excel_buffer.seek(0)
    
    return excel_buffer

async def create_tools_export(tools: list[Tool], lang: str) -> io.BytesIO:
    """Create Excel file with tools list"""
    wb = Workbook()
    ws = wb.active
    ws.title = get_text("tools_export_sheet", lang)

    # Styling
    header_font = Font(bold=True)
    header_fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
    center_align = Alignment(horizontal='center')

    # Headers
    headers = [
        get_text("excel_tool_id", lang),
        get_text("excel_tool_name", lang),
        get_text("excel_tool_status", lang),
        get_text("excel_tool_owner", lang),
        get_text("excel_tool_description", lang),
    ]

    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align

    # Data
    for row, tool in enumerate(tools, 2):
        ws.cell(row=row, column=1, value=tool.id)
        ws.cell(row=row, column=2, value=tool.name)
        ws.cell(row=row, column=3, value=get_text(f"tool_status_{tool.status}", lang))
        ws.cell(row=row, column=4, value=tool.user.user_enter_fio if tool.user else "-")
        ws.cell(row=row, column=5, value=tool.description or "-")

    # Column widths
    ws.column_dimensions['A'].width = 10  # ID
    ws.column_dimensions['B'].width = 30  # Name
    ws.column_dimensions['C'].width = 15  # Status
    ws.column_dimensions['D'].width = 30  # Owner
    ws.column_dimensions['E'].width = 40  # Description

    excel_buffer = io.BytesIO()
    wb.save(excel_buffer)
    excel_buffer.seek(0)
    
    return excel_buffer


async def create_materials_excel(materials: list, lang: str) -> io.BytesIO:
    """Create Excel file with materials list"""
    wb = Workbook()
    ws = wb.active
    ws.title = get_text("materials_sheet_name", lang)

    # Styles
    header_font = Font(bold=True)
    header_fill = PatternFill(start_color="CCCCCC", end_color="CCCCCC", fill_type="solid")
    center_align = Alignment(horizontal='center', vertical='center')

    # Headers
    headers = [
        get_text("excel_material_id", lang),
        get_text("excel_material_description", lang),
        get_text("excel_material_location", lang)
    ]

    for col, header in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col)
        cell.value = header
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center_align

    # Data
    for row, material in enumerate(materials, 2):
        ws.cell(row=row, column=1, value=material.id)
        ws.cell(row=row, column=2, value=material.description)
        ws.cell(row=row, column=3, value=material.storage_location or "-")

    # Adjust column widths
    ws.column_dimensions['A'].width = 10  # ID
    ws.column_dimensions['B'].width = 50  # Description
    ws.column_dimensions['C'].width = 30  # Location

    excel_buffer = io.BytesIO()
    wb.save(excel_buffer)
    excel_buffer.seek(0)
    
    return excel_buffer