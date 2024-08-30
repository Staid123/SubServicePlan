FROM python:3.10

# Установка системных зависимостей
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создание директории для приложения и установка рабочей директории
RUN mkdir /service
WORKDIR /service

# Копирование только файлов зависимостей
COPY requirements.txt ./

# Установка зависимостей Python
RUN pip install --no-cache-dir -r requirements.txt

# Копирование остального кода приложения
COPY service/ .

# Открытие портов
EXPOSE 8000

