FROM python:3.10-slim

# Встановлюємо необхідні залежності
RUN apt-get update && apt-get install -y libpq-dev gcc

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файл requirements.txt та встановлюємо залежності
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо всі файли додатку
COPY . /app

# Запуск Django сервера
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
