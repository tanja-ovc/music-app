FROM python:3.10-slim

RUN mkdir /app

COPY requirements.txt /app

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY qortexmusic/ /app

WORKDIR /app

CMD ["gunicorn", "qortexmusic.wsgi:application", "--bind", "0:8000" ]