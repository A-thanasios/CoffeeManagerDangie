import sqlite3
from sys import implementation

from Module import Product


def insert_product(db_path: str, product: Product, purchase_id: int) :
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO product (
                                purchase_id,
                                brand_name,
                                     shop,
                                     cost)
                VALUES (?, ?, ?, ?)
            ''', (
                purchase_id,
                product.brand_name,
                product.shop,
                product.cost))

            product_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            return product_id

    except sqlite3.Error as error:
        raise sqlite3.Error (error)

def select_product_by_id(db_path, product_id):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(__get_product_query() + 'WHERE purchase_id = ?', (product_id,))
            row = cursor.fetchone()
            if row:
                return __create_product(row)
            return None
    except sqlite3.Error as error:
        raise sqlite3.Error (error)

def select_products_by_purchase_id(db_path: str, purchase_id: int):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(__get_product_query() + 'WHERE purchase_id = ?', (purchase_id,))
            rows = cursor.fetchall()
            return __create_products_list(rows)
    except sqlite3.Error as error:
        raise sqlite3.Error (error)


def select_all_products(db_path: str):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(__get_product_query())
            rows = cursor.fetchall()
            return __create_products_list(rows)

    except sqlite3.Error as error:
        raise sqlite3.Error (error)


def update_product(db_path: str, product: Product):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE product
                SET brand_name = ?,
                    shop = ?,
                    cost = ?
                WHERE id = ?
            ''', (
                product.brand_name,
                product.shop,
                product.cost,
                product.id))

            # Check if the update was successful
            if cursor.rowcount == 0:
                raise sqlite3.Error(f"No product found with ID {product.id}")

            conn.commit()
    except sqlite3.Error as error:
        raise sqlite3.Error (error)

def delete_product_by_id(db_path: str, product_id: int):
    raise not implementation

def __get_product_query():
    return '''
           SELECT id,
                  brand_name,
                  shop,
                  cost
           FROM product
            '''

def __create_product(row):
    brand_name = row[1]
    shop = row[2]
    cost = row[3]
    db_id = row[0]
    return Product(brand_name, shop, cost, db_id)

def __create_products_list(rows):
    products = []
    for row in rows:
        products.append(__create_product(row))
    return products