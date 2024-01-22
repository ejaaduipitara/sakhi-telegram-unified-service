# syntax=docker/dockerfile:1

FROM python:3.13.0a2-slim

COPY / /app
WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT ["bash","script.sh"]