# Базовый Python образ
FROM python:3.11-slim

# Отключаем создание .pyc и буферизацию stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Рабочая директория
WORKDIR /app

# Системные зависимости (минимум)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Если используешь .env (НЕ для production)
COPY .env .env

# Запуск бота
CMD ["python", "run.py"]
