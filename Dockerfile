FROM python:3.11-alpine

WORKDIR /opt/services/

COPY requirements.txt /

COPY . .

RUN pip install -r requirements.txt

