FROM python:3.12

# Установка системных зависимостей
USER root
RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Создаем группу с GID 1000
RUN groupadd -g 1000 celerygroup

# Создаем пользователя с UID 1000 и добавляем в группу
RUN useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash celeryuser

# Настраиваем права ДО переключения пользователя
RUN mkdir -p /app/media && \
    chown celeryuser:celerygroup /app/media

# Копируем файлы с правильным владельцем
COPY --chown=celeryuser:celerygroup . /app

# Настраиваем права для скриптов
RUN chmod +x /app/wait-for-db.sh

# Переключаемся на непривилегированного пользователя
USER celeryuser

# Установка зависимостей и запуск
WORKDIR /app
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --only main

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]