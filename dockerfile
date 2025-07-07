FROM python:3.12-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libtesseract-dev \
    tesseract-ocr-rus \
    tesseract-ocr-eng \
    poppler-utils \
    ghostscript \
    && apt-get clean && rm -rf /var/lib/apt/lists/*


WORKDIR /app


COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt


COPY . /app