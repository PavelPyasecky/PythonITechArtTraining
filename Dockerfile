# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /gamestore

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . /gamestore

CMD [ "python3", "manage.py", "runserver"]
