FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements /app/requirements
RUN pip install --no-cache-dir -r requirements/production.txt

COPY . /app