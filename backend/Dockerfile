# syntax=docker/dockerfile:1

# Base Python image & dependencies
FROM python:3.11-slim AS base
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Development target
FROM base AS dev
WORKDIR /app
# copy code
COPY . /app
# SQLite file will live in /database (mounted volume)
ENV DATABASE_URL=sqlite:////database_data/app.db
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production target
FROM base AS prod
WORKDIR /app
COPY . /app
ENV DATABASE_URL=sqlite:////database_data/app.db
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
