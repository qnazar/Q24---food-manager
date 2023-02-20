import psycopg2
import os
import csv

connection = psycopg2.connect(
    dbname=os.environ.get('PG_DATABASE'),
    user=os.environ.get('PG_USER'),
    password=os.environ.get('PG_PSSWRD'),
    host=os.environ.get('PG_HOST'),
    port=os.environ.get('PG_PORT')
)
connection.autocommit = True
cursor = connection.cursor()

category_query = """INSERT INTO product_category (id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING"""
with open('/data/product_categories', 'r') as file:
    categories_reader = csv.reader(file)
    for row in categories_reader:
        cursor.execute(category_query, row)

product_query = """INSERT INTO product (id, name, kcal, proteins, fats, carbs, fibers, category_id) 
VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"""
with open('/data/products', 'r') as file:
    products_reader = csv.reader(file)
    for row in products_reader:
        cursor.execute(product_query, row)

cursor.close()
connection.close()
