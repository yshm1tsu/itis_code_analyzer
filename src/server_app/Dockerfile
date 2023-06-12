FROM python:3.8

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

ENV PORT 8000
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY .. .
CMD mkdir aws/
COPY config aws/
COPY credentials .aws/
CMD uwsgi --http :$PORT --wsgi-file app.py
