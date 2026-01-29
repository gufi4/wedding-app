# Этап 1: Сборка зависимостей
FROM python:3.11-slim as builder

WORKDIR /app

# Системные зависимости для сборки
RUN apt-get update && apt-get install -y gcc && rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем Python зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Этап 2: Финальный образ
FROM python:3.11-slim

WORKDIR /app

# Runtime зависимости
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Копируем зависимости из builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Копируем код приложения
COPY . .

# Создаём папку для базы данных
RUN mkdir -p /app/data

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

CMD ["python", "main.py"]
