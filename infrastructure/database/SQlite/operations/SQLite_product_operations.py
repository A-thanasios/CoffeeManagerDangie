import sqlite3

from Module import Product


def insert_product(db_path: str, product: Product, purchase_id: int):
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

            new_id = cursor.lastrowid
            product.id = new_id
            conn.commit()
            cursor.close()
            return new_id
    except sqlite3.Error as error:
        raise sqlite3.Error (error)

def get_product_by_id(db_path, product_id):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(__get_product_query(), (product_id,))
            row = cursor.fetchone()
            if row:
                return __create_product(row)
            return None
    except sqlite3.Error as error:
        raise sqlite3.Error (error)

def get_products_by_purchase_id(db_path: str, purchase_id: int):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(__get_product_query(), (purchase_id,))
            rows = cursor.fetchall()
            __create_products_list(rows)
    except sqlite3.Error as error:
        raise sqlite3.Error (error)


def get_all_products(db_path: str):
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
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM product WHERE id = ?',
                           (product_id,))
            conn.commit()
    except sqlite3.Error as error:
        raise sqlite3.Error (error)

def __get_product_query():
    return '''
           SELECT id,
                  brand_name,
                  shop,
                  cost
           FROM product
           WHERE purchase_id = ? \
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