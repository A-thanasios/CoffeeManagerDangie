import sqlite3

from database.db_setup import logger
from database.operations.db_coffee_operations import get_coffee_by_id
from database.operations.db_person_operations import get_person_by_id
from src.data.purchase import Purchase


def insert_purchase(db_path, purchase):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # insert purchase
            cursor.execute('''
                INSERT INTO purchase (name, date)
                VALUES (?, ?)
            ''', (purchase.name, purchase.date))
            purchase_id = cursor.lastrowid

            # insert relationships with persons
            for person in purchase.persons:
                cursor.execute('''
                    INSERT INTO purchase_person (purchase_id, person_id)
                    VALUES (?, ?)
                ''', (purchase_id, person.id))

            # insert relationships with coffees
            for coffee in purchase.coffees:
                cursor.execute('''
                    INSERT INTO purchase_coffee (purchase_id, coffee_id)
                    VALUES (?, ?)
                ''', (purchase_id, coffee.id))

            conn.commit()
            return purchase_id
    except sqlite3.Error as error:
        logger.error(error)
        raise


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

            # get persons
            cursor.execute('''
                SELECT person_id FROM purchase_person WHERE purchase_id = ?
            ''', (purchase_id,))
            persons = [get_person_by_id(db_path, row[0]) for row in cursor.fetchall()]

            # get coffees
            cursor.execute('''
                SELECT coffee_id FROM purchase_coffee WHERE purchase_id = ?
            ''', (purchase_id,))
            coffees = [get_coffee_by_id(db_path, row[0]) for row in cursor.fetchall()]

            return Purchase(purchase_row[1], persons, coffees, purchase_row[2], purchase_row[0])
    except sqlite3.Error as error:
        logger.error(error)
        raise


def get_purchases_by_person(db_path, person_id):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, name, date, coffee_id
                FROM purchase WHERE person_id = ?
            ''', (person_id,))
            rows = cursor.fetchall()
            purchases = []
            for row in rows:
                coffee = get_coffee_by_id(db_path, row[3])
                person = get_person_by_id(db_path, person_id)
                purchases.append(Purchase(row[1], [person], coffee, row[2]))
            return purchases
    except sqlite3.Error as error:
        logger.error(error)
        raise




