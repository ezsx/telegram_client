# Используем базовый образ с Python
FROM python:3.9-slim

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем скрипты в контейнер
WORKDIR /app
COPY . /app

# Указываем команду для запуска скрипта
CMD ["python", "main.py"]
