import traceback
import gspread
from aiogram.types import Message
from google.oauth2.service_account import Credentials
from datetime import datetime

from loguru import logger

from app.db.schemas import ObjectMaterialOrderModel

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
SERVICE_ACCOUNT_FILE = "seraphic-amp-444606-u5-9640c5f896bc.json" 

def get_gsheet_client():
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return gspread.authorize(creds)

def append_object_material_order_to_sheet(order: ObjectMaterialOrderModel, sent_message:Message, spreadsheet_id: str, worksheet_name: str):
    try:
        client = get_gsheet_client()
        sheet = client.open_by_key(spreadsheet_id).worksheet(worksheet_name)

        chat_id = str(sent_message.chat.id)
        if chat_id.startswith("-100"):
            tg_chat_id = chat_id[4:]  # убираем -100
            message_link = f"https://t.me/c/{tg_chat_id}/{sent_message.message_id}"
        else:
            message_link = "-"

        # Собираем строку для вставки
        row = [
            datetime.now().strftime("%d.%m.%Y %H:%M:%S"),  # Отметка времени
            datetime.now().strftime("%d.%m.%Y"),           # Дата заявки
            order.delivery_date or "-",                    # Дата поставки
            getattr(order, "object_name", "-"),            # Объект
            message_link,                                  # Ссылка на заявку
            "-",                                           # Итоговая стоимость
            order.description or "-",                      # Материал
            "-",                                           # Дата оплаты
            "В работе",                                    # Статус (по умолчанию)
        ]
        sheet.append_row(row, value_input_option="USER_ENTERED")
    except Exception as e:
        logger.error(
            f"Ошибка при добавлении заказа в Google Sheets: {e}\n"
            f"spreadsheet_id={spreadsheet_id}, worksheet_name={worksheet_name}, row={row if 'row' in locals() else 'not built'}\n"
            f"{traceback.format_exc()}"
        )
        raise e