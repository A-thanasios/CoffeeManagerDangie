import sqlite3
from datetime import datetime

from infrastructure.database.SQlite.operations.SQLite_product_operations import get_product_by_id
from infrastructure.database.SQlite.operations.SQLite_person_operations import get_person_by_id
from module.data.purchase import Purchase


# This module contains functions to interact with the purchase table in the database.

# insert functions
def insert_purchase(db_path, purchase):
    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()

            # Insert purchase with ISO formatted date
            cursor.execute('''
                INSERT INTO purchase (name, date)
                VALUES (?, datetime(?))
            ''', (purchase.name, purchase.date.isoformat()))
            purchase_id = cursor.lastrowid

            # Insert relationships with persons
            for person in purchase.persons:
                cursor.execute('''
                    INSERT INTO purchase_person (purchase_id, person_id)
                    VALUES (?, ?)
                ''', (purchase_id, person.id))

            # Insert relationships with products
            for product in purchase.products:
                cursor.execute('''
                    INSERT INTO purchase_product (purchase_id, product_id)
                    VALUES (?, ?)
                ''', (purchase_id, product.id))

            conn.commit()
            return purchase_id
    except sqlite3.Error as error:
        raise sqlite3.Error (error)


# get functions

def get_purchase_by_id(db_path, purchase_id):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # get purchase
            cursor.execute('''
                SELECT id, name, date FROM purchase WHERE id = ?
            ''', (purchase_id,))
            purchase_row = cursor.fetchone()

            if not purchase_row:
                return None

            # Convert date to datetime object
            purchase_date = datetime.strptime(purchase_row[2], "%Y-%m-%d %H:%M:%S")

            # get persons
            cursor.execute('''
                SELECT person_id FROM purchase_person WHERE purchase_id = ?
            ''', (purchase_id,))
            persons = [get_person_by_id(db_path, row[0]) for row in cursor.fetchall()]

            # get products
            cursor.execute('''
                SELECT product_id FROM purchase_product WHERE purchase_id = ?
            ''', (purchase_id,))
            products = [get_product_by_id(db_path, row[0]) for row in cursor.fetchall()]

            return Purchase(purchase_row[1], persons, products, purchase_date, purchase_row[0])
    except sqlite3.Error as error:
        raise sqlite3.Error (error)


def get_purchases_by_person_id(db_path, person_id):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT p.id, p.name, p.date
                FROM purchase AS p
                JOIN purchase_person AS pp ON p.id = pp.purchase_id
                WHERE pp.person_id = ?
            ''', (person_id,))
            rows = cursor.fetchall()

            purchases = []
            for row in rows:
                purchase_id, purchase_name, purchase_date_str = row

                cursor.execute('''
                    SELECT product_id
                    FROM purchase_product
                    WHERE purchase_id = ?
                ''', (purchase_id,))
                product_ids = [r[0] for r in cursor.fetchall()]
                products = [get_product_by_id(db_path, pid) for pid in product_ids]

                person = get_person_by_id(db_path, person_id)

                purchase_date = datetime.strptime(purchase_date_str, "%Y-%m-%d %H:%M:%S")

                purchases.append(Purchase(purchase_name, [person], products, purchase_date, purchase_id))

            return purchases
    except sqlite3.Error as error:
        raise sqlite3.Error(error)

def get_all_purchases(db_path):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, date
                FROM purchase
            ''')
            rows = cursor.fetchall()
            purchases = []
            for row in rows:
                purchases.append(get_purchase_by_id(db_path, row[0]))
            return purchases
    except sqlite3.Error as error:
        raise sqlite3.Error (error)

def update_purchase(db_path, purchase):
    try:
        with sqlite3.connect(db_path) as conn:
            # Enable foreign key support
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()

            # Update main purchase record with ISO formatted date
            cursor.execute('''
                UPDATE purchase
                SET name = ?, date = datetime(?)
                WHERE id = ?
            ''', (purchase.name, purchase.date.isoformat(), purchase.id))

            # Check if record exists
            if cursor.rowcount == 0:
                raise sqlite3.Error(f"No purchase found with ID {purchase.id}")

            # Clear existing relationships
            cursor.execute('DELETE FROM purchase_person WHERE purchase_id = ?', (purchase.id,))
            cursor.execute('DELETE FROM purchase_product WHERE purchase_id = ?', (purchase.id,))

            # Insert updated person relationships
            for person in purchase.persons:
                cursor.execute('''
                    INSERT INTO purchase_person (purchase_id, person_id)
                    VALUES (?, ?)
                ''', (purchase.id, person.id))

            # Insert updated product relationships
            for product in purchase.products:
                cursor.execute('''
                    INSERT INTO purchase_product (purchase_id, product_id)
                    VALUES (?, ?)
                ''', (purchase.id, product.id))

            conn.commit()
    except sqlite3.Error as error:
        raise sqlite3.Error (error)

def delete_purchase_by_id(db_path, purchase_id):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM purchase WHERE id = ?
            ''', (purchase_id,))

            if cursor.rowcount == 0:
                raise sqlite3.Error(f"No purchase found with ID {purchase_id}")

            conn.commit()
    except sqlite3.Error as error:
        raise sqlite3.Error (error)

