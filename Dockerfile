# Багатоетапна збірка для оптимізації розміру образу
# Етап 1: Встановлення залежностей
FROM python:3.11-slim AS builder

WORKDIR /app

# Копіюємо файл з залежностями
COPY requirements.txt .

# Встановлюємо залежності у користувацьку директорію
RUN pip install --no-cache-dir --user -r requirements.txt

# Етап 2: Фінальний образ з легким Alpine базовим образом
FROM python:3.11-alpine

# Встановлюємо wget для health check
RUN apk add --no-cache wget

WORKDIR /app

# Копіюємо встановлені пакети з етапу збірки
COPY --from=builder /root/.local /root/.local

# Додаємо встановлені пакети до PATH
ENV PATH=/root/.local/bin:$PATH

# Створюємо директорію для бази даних
RUN mkdir -p /app/data && chmod 755 /app/data

# Копіюємо код застосунку
COPY . .

# Налаштування змінних середовища
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV DATABASE_PATH=/app/data/database.db
ENV PYTHONUNBUFFERED=1

# Відкриваємо порт
EXPOSE 5000

# Health check - перевірка доступності застосунку
HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:5000/ || exit 1

# Команда запуску застосунку
CMD ["python", "app.py"]
