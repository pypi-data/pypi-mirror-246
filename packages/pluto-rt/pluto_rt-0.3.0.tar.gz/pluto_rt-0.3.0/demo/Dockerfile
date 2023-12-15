# syntax=docker/dockerfile:1
FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/code
WORKDIR /code
COPY demo/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . /code
RUN pip install .
EXPOSE 8000
