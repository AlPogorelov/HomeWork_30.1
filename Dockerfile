FROM python:3.12

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install -- no-cache-dir -r requirements.txt

COPY . .

ENV SECRET_KEY="django-insecure-ine9%aw^=!ptp3&nfr)97h-7avugu2^nrkm77jg=-d2xd1v(8d"
ENV CELERY_BROKER_URL='redis://localhost:6379'
ENV CELERY_BACKEND='redis://localhost:6379'

RUN mkdir -p /app/media

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]