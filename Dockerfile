FROM python:3.10-slim

WORKDIR /app

# Продакшен-зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Приложение
COPY tools/ ./tools/
COPY main.py .
COPY templates/ ./templates/
COPY static/ ./static/

# Открываем порт
EXPOSE 5000

# Запускаем приложение
CMD ["python", "main.py"]