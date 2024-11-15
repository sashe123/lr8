import psycopg2
import time

retries = 5
while retries > 0:
    try:
        connection = psycopg2.connect(
            dbname="mydatabase",
            user="myuser",
            password="mypassword",
            host="db",
            port="5432"
        )
        break
    except psycopg2.OperationalError:
        retries -= 1
        print("База даних ще не готова, повторюємо спробу через 5 секунд...")
        time.sleep(5)
else:
    raise Exception("Не вдалося підключитися до бази даних")

connection.autocommit = True
cursor = connection.cursor()

print('Починаю створювати таблиці')

# Створення таблиці "Помилки" з необхідними властивостями полів
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Errors (
        error_code SERIAL PRIMARY KEY,
        error_description TEXT NOT NULL,
        received_date DATE NOT NULL,
        error_level VARCHAR(50) NOT NULL CHECK (error_level IN ('критична', 'важлива', 'незначна')),
        functionality_category VARCHAR(50) NOT NULL CHECK (functionality_category IN ('інтерфейс', 'дані', 'розрахунковий алгоритм', 'інше', 'невідома категорія')),
        error_source VARCHAR(50) NOT NULL CHECK (error_source IN ('користувач', 'тестувальник'))
    );
''')

# Створення таблиці "Програмісти" з необхідними властивостями полів
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Programmers (
        programmer_code SERIAL PRIMARY KEY,
        last_name VARCHAR(100) NOT NULL,
        first_name VARCHAR(100) NOT NULL,
        phone_number VARCHAR(20) NOT NULL CHECK (phone_number ~ '^\+380\d{9}$')
    );
''')

# Створення таблиці "Виправлення помилок" з необхідними властивостями полів
cursor.execute('''
    CREATE TABLE IF NOT EXISTS BugFixes (
        fix_code SERIAL PRIMARY KEY,
        error_code INTEGER REFERENCES Errors(error_code),
        start_date DATE NOT NULL,
        duration_days INTEGER NOT NULL CHECK (duration_days IN (1, 2, 3)),
        programmer_code INTEGER REFERENCES Programmers(programmer_code),
        cost_per_day DECIMAL(10, 2) NOT NULL DEFAULT 1000.00 CHECK (cost_per_day > 0)
    );
''')

# Закриття курсора та з'єднання
cursor.close()
connection.close()

print('Таблиці створено')