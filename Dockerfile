FROM alpine
MAINTAINER <branlewalk@gmail.com>
FROM python:3.7

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
