FROM python:3.12

# 1. Установка зависимостей и настройка от root
USER root

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 2. Создание пользователя с явным UID/GID
RUN adduser --disabled-password --gecos '' --uid 1000 --gid 1000 celeryuser

# 3. Все операции с правами выполняем ОТ root ДО переключения пользователя
RUN mkdir -p /app/media && \
    chown celeryuser:celeryuser /app/media

# 4. Копирование файлов с правильным владельцем
COPY --chown=celeryuser:celeryuser . /app

# 5. Настройка прав для скриптов
RUN chmod +x /app/wait-for-db.sh

# 6. Переключение на непривилегированного пользователя
USER celeryuser

# 7. Рабочая директория и остальные инструкции
WORKDIR /app
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --only main

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]