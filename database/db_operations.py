import sqlite3

from database.db_setup import logger
from src.data.coffee import Coffee
from src.data.person import Person
from src.data.purchase import Purchase
from src.data.structs.name import Name


def insert_person(db_path, person):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO person (first_name, middle_name, last_name, days_per_week, is_buying, img)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (person.name.first_name, person.name.middle_name, person.name.last_name,
                  person.days_per_week, person.is_buying, person.img))

            new_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            return new_id
    except sqlite3.Error as error:
        logger.error(error)
        raise

def get_person_by_id(db_path, person_id):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, first_name, middle_name, last_name, days_per_week, is_buying, img 
                FROM person WHERE id = ?
            ''', (person_id,))
            row = cursor.fetchone()
            if row:
                name = Name(row[1], row[2], row[3])
                return Person(name, row[4], row[5], row[6], row[0])
            return None
    except sqlite3.Error as error:
        logger.error(error)
        raise

def insert_coffee(db_path, coffee):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO coffee (brand_name, shop, cost, img)
                VALUES (?, ?, ?, ?)
            ''', (coffee.brand_name, coffee.shop, coffee.cost, coffee.img))

            new_id = cursor.lastrowid
            conn.commit()
            cursor.close()
            return new_id
    except sqlite3.Error as error:
        logger.error(error)
        raise

def get_coffee_by_id(db_path, coffee_id):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, brand_name, shop, cost, img
                FROM coffee WHERE id = ?
            ''', (coffee_id,))
            row = cursor.fetchone()
            if row:
                return Coffee(row[1], row[2], row[3], row[4], row[0])
            return None
    except sqlite3.Error as error:
        logger.error(error)
        raise


def insert_purchase(db_path, purchase):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Vložení základního nákupu
            cursor.execute('''
                INSERT INTO purchase (name, date)
                VALUES (?, ?)
            ''', (purchase.name, purchase.date))
            purchase_id = cursor.lastrowid

            # Vložení vazeb na osoby
            for person in purchase.persons:
                cursor.execute('''
                    INSERT INTO purchase_person (purchase_id, person_id)
                    VALUES (?, ?)
                ''', (purchase_id, person.id))

            # Vložení vazeb na kávy
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




