# -*- coding: utf-8 -*-
import psycopg2
import bcrypt
from datetime import datetime

conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="12345",
    host="localhost",
    port="5432"
)

# Open a cursor to perform database operations
cursor = conn.cursor()

# Execute a query
for i in range(1, 11):
    cursor.execute("INSERT INTO users (created_at, name, email, phone, password, confirmed) "
                   "VALUES (%s, %s, %s, %s, %s, %s)", (
                       datetime.utcnow(),
                       f"test{i}@test.com",
                       f"test{i}@test.com",
                       "+79519360868",
                       bcrypt.hashpw("1@yAndexru".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
                       True))

for i in range(6):
    cursor.execute("INSERT INTO transactions_categories (created_at, name, parent_category_id) "
                   "VALUES (%s, %s, %s)", (
                       datetime.utcnow(),
                       f"Тестовая категория {i}",
                       i))

conn.commit()
cursor.close()
conn.close()
