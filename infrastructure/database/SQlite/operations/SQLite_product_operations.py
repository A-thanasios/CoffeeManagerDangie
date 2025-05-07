import sqlite3

from module.model.product import Product


def insert_product(db_path, product):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO product (brand_name, shop, cost, img)
                VALUES (?, ?, ?, ?)
            ''', (product.brand_name, product.shop, product.cost, product.img))

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
            cursor.execute('''
                SELECT id, brand_name, shop, cost, img
                FROM product WHERE id = ?
            ''', (product_id,))
            row = cursor.fetchone()
            if row:
                return Product(row[1], row[2], row[3], row[4], row[0])
            return None
    except sqlite3.Error as error:
        raise sqlite3.Error (error)

def get_products_by_person_id(db_path, person_id):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT c.id, c.brand_name, c.shop, c.cost, c.img
            FROM product AS c
            JOIN purchase_product AS pc ON c.id = pc.product_id
            JOIN purchase_person AS pp ON pc.purchase_id = pp.purchase_id
            JOIN person AS p ON pp.person_id = p.id
            WHERE p.id = ?
            ''', (person_id,))
            rows = cursor.fetchall()
            products = []
            for row in rows:
                products.append(Product(row[1], row[2], row[3], row[4], row[0]))
            return products
    except sqlite3.Error as error:
        raise sqlite3.Error (error)

def get_all_products(db_path):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, brand_name, shop, cost, img
                FROM product
            ''')
            rows = cursor.fetchall()
            products = []
            for row in rows:
                products.append(Product(row[1], row[2], row[3], row[4], row[0]))
            return products
    except sqlite3.Error as error:
        raise sqlite3.Error (error)


def update_product(db_path, product):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE product
                SET brand_name = ?, shop = ?, cost = ?, img = ?
                WHERE id = ?
            ''', (product.brand_name, product.shop, product.cost, product.img, product.id))
            # Check if the update was successful
            if cursor.rowcount == 0:
                raise sqlite3.Error(f"No product found with ID {product.id}")

            conn.commit()
    except sqlite3.Error as error:
        raise sqlite3.Error (error)

def delete_product_by_id(db_path, product_id):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM product WHERE id = ?
            ''', (product_id,))
            conn.commit()
    except sqlite3.Error as error:
        raise sqlite3.Error (error)