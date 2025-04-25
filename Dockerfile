FROM python:3.12

# Установка системных зависимостей от root
USER root

RUN mkdir -p /var/run/celery && \
    chown -R celeryuser:celeryuser /var/run/celery

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Создаем группу и пользователя
RUN groupadd -g 1000 celerygroup && \
    useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash celeryuser

# Настраиваем рабочие директории
RUN mkdir -p /app/media && \
    chown celeryuser:celerygroup /app/media

# Копируем файлы проекта
COPY --chown=celeryuser:celerygroup . /app

# Устанавливаем права для скриптов
RUN chmod +x /app/wait-for-db.sh

# Переключаемся на пользователя celeryuser
USER celeryuser
WORKDIR /app

# Настраиваем окружение
ENV PATH="/home/celeryuser/.local/bin:${PATH}"

# Устанавливаем Poetry и зависимости
RUN pip install --user poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --only main

COPY requirements.txt .
RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]