FROM python:3.10 as base

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["sh", "-c", "\
    sleep 10 && \
    python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py loaddata fixtures/*.json && \
    python manage.py runserver 0.0.0.0:8000"]