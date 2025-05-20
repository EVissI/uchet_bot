import io
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from datetime import datetime

from app.bot.common.texts import get_text
from app.db.models import ObjectCheck, Tool


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