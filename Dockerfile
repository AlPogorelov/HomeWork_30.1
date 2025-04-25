FROM python:3.12

# Установка системных зависимостей от root
USER root

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Создаем группу и пользователя с явным UID/GID
RUN groupadd -g 1000 celerygroup && \
    useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash celeryuser

# Создаем директории и настраиваем права
RUN mkdir -p /app/media && \
    chown celeryuser:celerygroup /app/media

# Копируем файлы с правильным владельцем
COPY --chown=celeryuser:celerygroup . /app

# Настраиваем права для скриптов
RUN chmod +x /app/wait-for-db.sh

# Переключаемся на непривилегированного пользователя
USER celeryuser

# Устанавливаем Poetry в пользовательский каталог и добавляем в PATH
ENV PATH="/home/celeryuser/.local/bin:${PATH}"
WORKDIR /app

# Установка зависимостей через Poetry
RUN pip install --user poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --only main

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]