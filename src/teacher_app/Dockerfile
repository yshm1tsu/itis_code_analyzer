FROM python:3.9

WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

RUN apt update && \
    apt install -yq --no-install-recommends binutils libproj-dev gdal-bin \
    postgresql-client libsasl2-dev libssl-dev && \
    pip install --upgrade pip poetry==1.1.12 && poetry config virtualenvs.create false
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-dev
COPY . .
CMD python src/manage.py migrate && uwsgi --ini deploy/python/uwsgi.ini
