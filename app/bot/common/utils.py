import random
from typing import Tuple

import re
import tempfile
from typing import Tuple, Optional
from PIL import Image
from loguru import logger
import pytesseract
from pdf2image import convert_from_bytes
from io import BytesIO


def generate_math_example() -> Tuple[str, int]:
    """
    Generates a simple math example with numbers from 1 to 20
    Returns tuple with example string and correct answer
    """
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    operation = '+'
    
    example = f"{a} {operation} {b}"
    
    answer = a + b
            
    return example, answer


def convert_pdf_to_jpg_bytes(pdf_file: bytes) -> Tuple[bytes, str]:
    """
    Конвертирует первую страницу PDF в JPEG.
    Возвращает JPEG в байтах и путь к временному JPG-файлу.
    """
    try:
        images = convert_from_bytes(pdf_file, dpi=300, fmt='jpeg')
    except Exception as e:
        logger.error(f"Ошибка при конвертации PDF: {e}")
        raise

    if not images:
        logger.error("PDF не содержит изображений или не удалось сконвертировать.")
        raise ValueError("Не удалось сконвертировать PDF в изображение")

    img: Image.Image = images[0]

    # Сохраняем во временный файл
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    img.save(temp_file, format='JPEG')
    temp_file.close()

    # Также сохраняем в байты для Telegram
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)

    return img_byte_arr.read(), temp_file.name


def extract_receipt_data(image_bytes: bytes) -> dict:
    """
    Извлекает дату и сумму из изображения чека для разных банков.
    """
    image = Image.open(BytesIO(image_bytes))
    text = pytesseract.image_to_string(image, lang='rus+eng')
    logger.debug(f"Извлечённый текст: {text}")

    data = {}

    # Паттерны для разных банков
    bank_patterns = {
        "tinkoff": {
            "date": r'(\d{2}\.\d{2}\.\d{4}(?:\s+\d{2}:\d{2}:\d{2})?)',
            "amount": r'(?:Сумма|Итого)\s+([\d\s]+(?:[.,]\d{2})?)\s*[₽Р]'
        },
        "sberbank": {
            "date": r'Дата:\s*(\d{2}\.\d{2}\.\d{4})',
            "amount": r'ИТОГ\s+([\d\s]+(?:[.,]\d{2})?)\s*₽'
        },
        "alfa": {
            "date": r'Дата операции:\s*(\d{2}\.\d{2}\.\d{4})',
            "amount": r'Сумма к оплате:\s*([\d\s]+(?:[.,]\d{2})?)\s*₽'
        }
    }

    # Пробуем определить банк и извлечь данные
    for bank, patterns in bank_patterns.items():
        date_match = re.search(patterns["date"], text)
        if date_match:
            data['date'] = date_match.group(1)
            amount_match = re.search(patterns["amount"], text, re.IGNORECASE)
            if amount_match:
                amount = amount_match.group(1).replace(' ', '').replace(',', '.')
                data['amount'] = amount
                data['bank'] = bank
                break

    logger.debug(f"Извлечённые данные: {data}")
    return data if data else {"date": None, "amount": None}
