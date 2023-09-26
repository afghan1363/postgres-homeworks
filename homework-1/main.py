"""Скрипт для заполнения данными таблиц в БД Postgres."""
import os.path
import psycopg2
import csv

employees_data = os.path.join('north_data', 'employees_data.csv')
customers_data = os.path.join('north_data', 'customers_data.csv')
orders_data = os.path.join('north_data', 'orders_data.csv')
password = input("Enter the password for user postgres ")
connect_to_db = psycopg2.connect(
    host="localhost",
    database="north",
    user="postgres",
    password=password
)
with connect_to_db:
    with connect_to_db.cursor() as cursor:
        try:
            with open(employees_data) as file:
                csv_data = csv.DictReader(file, delimiter=',')

                for row in csv_data:
                    first_name = row['first_name']
                    last_name = row['last_name']
                    title = row['title']
                    birth_date = row['birth_date']
                    notes = row['notes']

                    cursor.executemany(
                        'INSERT INTO employees VALUES (default, %s, %s, %s, %s, %s)',
                        [(first_name, last_name, title, birth_date, notes)])
        except FileNotFoundError:
            print("Файл employees_data не найден")
        except KeyError:
            print("Ошибка данных employees_data")

        try:
            with open(customers_data) as file:
                csv_data = csv.DictReader(file, delimiter=',')

                for row in csv_data:
                    customer_id = row['customer_id']
                    company_name = row['company_name']
                    contact_name = row['contact_name']

                    cursor.executemany(
                        'INSERT INTO customers VALUES (%s, %s, %s)',
                        [(customer_id, company_name, contact_name)])
        except FileNotFoundError:
            print("Файл customers_data не найден")
        except KeyError:
            print("Ошибка данных customers_data")

        try:
            with open(orders_data) as file:
                csv_data = csv.DictReader(file, delimiter=',')

                for row in csv_data:
                    order_id = row['order_id']
                    customer_id = row['customer_id']
                    employee_id = row['employee_id']
                    order_date = row['order_date']
                    ship_city = row['ship_city']

                    cursor.executemany(
                        'INSERT INTO orders VALUES (%s, %s, %s, %s, %s)',
                        [(order_id, customer_id, employee_id, order_date, ship_city)])
        except FileNotFoundError:
            print("Файл orders_data не найден")
        except KeyError:
            print("Ошибка данных orders_data")
connect_to_db.close()
