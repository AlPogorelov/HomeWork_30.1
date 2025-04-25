FROM python:3.12

# Установка системных зависимостей

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app

# Копирование зависимостей отдельным слоем для кэширования
COPY --chown=celeryuser:celeryuser pyproject.toml poetry.lock ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

# Установка Poetry и зависимостей
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --only main

# Копирование остальных файлов
COPY --chown=celeryuser:celeryuser . .

# Настройка прав
RUN chmod +x /app/wait-for-db.sh && \
    mkdir -p /app/media && \
    chown celeryuser:celeryuser /app/media

# Переключаемся на непривилегированного пользователя
USER celeryuser

EXPOSE 8000

# ОДНА команда CMD
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]