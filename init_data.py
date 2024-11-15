import psycopg2
from psycopg2 import sql
import faker
import random
from datetime import datetime, timedelta
import time
from tabulate import tabulate

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

print('Починаю генерувати дані')

# Ініціалізація Faker
fake = faker.Faker()

# Додавання 20 записів у таблицю "Помилки"
error_levels = ['критична', 'важлива', 'незначна']
functionality_categories = ['інтерфейс', 'дані', 'розрахунковий алгоритм', 'інше', 'невідома категорія']
error_sources = ['користувач', 'тестувальник']

for _ in range(20):
    error_description = fake.sentence()
    received_date = fake.date_between(start_date="-1y", end_date="today")
    error_level = random.choice(error_levels)
    functionality_category = random.choice(functionality_categories)
    error_source = random.choice(error_sources)

    cursor.execute('''
        INSERT INTO Errors (error_description, received_date, error_level, functionality_category, error_source)
        VALUES (%s, %s, %s, %s, %s);
    ''', (error_description, received_date, error_level, functionality_category, error_source))

# Додавання 4 записів у таблицю "Програмісти"
for _ in range(4):
    last_name = fake.last_name()
    first_name = fake.first_name()
    phone_number = f'+380{fake.random_number(digits=9, fix_len=True)}'  # Форматуємо номер як +380XXXXXXXXX

    cursor.execute('''
        INSERT INTO Programmers (last_name, first_name, phone_number)
        VALUES (%s, %s, %s);
    ''', (last_name, first_name, phone_number))

# Отримати всі існуючі програмістські коди з таблиці "Програмісти"
cursor.execute('SELECT programmer_code FROM Programmers')
programmer_codes = [row[0] for row in cursor.fetchall()]

# Додавання 10 записів у таблицю "Виправлення помилок"
for _ in range(10):
    error_code = random.randint(1, 20)  # Випадковий код помилки (з припущенням, що у нас 20 помилок)
    start_date = fake.date_between(start_date="-6m", end_date="today")
    duration_days = random.choice([1, 2, 3])
    programmer_code = random.choice(programmer_codes)  # Випадковий існуючий код програміста
    cost_per_day = random.randint(1000, 3000)

    cursor.execute('''
        INSERT INTO BugFixes (error_code, start_date, duration_days, programmer_code, cost_per_day)
        VALUES (%s, %s, %s, %s, %s);
    ''', (error_code, start_date, duration_days, programmer_code, cost_per_day))

print('Створюю запити до БД')

# # Запити до бази даних
# queries = [
#     # Відобразити всі критичні помилки. Відсортувати по коду помилки
#     "SELECT * FROM errors WHERE error_level = 'критична' ORDER BY error_code;",

#     # Порахувати кількість помилок кожного рівня (підсумковий запит)
#     "SELECT error_level, COUNT(*) AS count FROM errors GROUP BY error_level;",

#     # Порахувати вартість роботи програміста при виправленні кожної помилки (запит з обчислювальним полем)
#     "SELECT fix_code, error_code, programmer_code, duration_days, cost_per_day, (duration_days * cost_per_day) AS total_cost FROM BugFixes;",

#     # Відобразити всі помилки, які надійшли із заданого джерела (запит з параметром)
#     "SELECT * FROM errors WHERE error_source = %s;",

#     # Порахувати кількість помилок, які надійшли від користувачів та тестувальників (підсумковий запит)
#     "SELECT error_source, COUNT(*) AS count FROM errors GROUP BY error_source;",

#     # Порахувати кількість критичних, важливих, незначних помилок, виправлених кожним програмістом (перехресний запит)
#     "SELECT p.programmer_code, p.last_name, p.first_name, e.error_level, COUNT(*) AS count \
#      FROM BugFixes bf \
#      JOIN Programmers p ON bf.programmer_code = p.programmer_code \
#      JOIN errors e ON bf.error_code = e.error_code \
#      GROUP BY p.programmer_code, p.last_name, p.first_name, e.error_level;"
# ]

# # Виконання запитів та вивід результатів у консоль з форматуванням
# for query in queries:
#     if query == queries[3]:
#         cursor.execute(query, ('користувач',))  # Приклад виконання запиту з параметром
#     else:
#         cursor.execute(query)
#     rows = cursor.fetchall()
#     print(f"\nЗапит: {query}\n")
#     if rows:
#         headers = [desc[0] for desc in cursor.description]
#         print(tabulate(rows, headers=headers, tablefmt='pretty'))
#     else:
#         print("Немає даних для відображення")

# # Вивід структури та даних таблиць з форматуванням
# tables = ['errors', 'programmers', 'bugfixes']
# for table in tables:
#     print(f"\nТаблиця: {table}\n")
#     cursor.execute(sql.SQL("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = %s"), [table])
#     columns = cursor.fetchall()
#     print("Структура таблиці:")
#     print(tabulate(columns, headers=['Column Name', 'Data Type'], tablefmt='pretty'))

#     cursor.execute(sql.SQL(f"SELECT * FROM {table}"))
#     rows = cursor.fetchall()
#     print("Дані таблиці:")
#     if rows:
#         headers = [desc[0] for desc in cursor.description]
#         print(tabulate(rows, headers=headers, tablefmt='pretty'))
#     else:
#         print("Немає даних для відображення")

# Закриття курсора та з'єднання
cursor.close()
connection.close()

print("Запити та структури відображені")
