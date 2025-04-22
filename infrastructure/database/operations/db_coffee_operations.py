import sqlite3

from infrastructure.database.SQLite_database import logger
from module.data.coffee import Coffee


def insert_coffee(db_path, coffee):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO coffee (brand_name, shop, cost, img)
                VALUES (?, ?, ?, ?)
            ''', (coffee.brand_name, coffee.shop, coffee.cost, coffee.img))

            new_id = cursor.lastrowid
            coffee.id = new_id
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
def get_coffees_by_person_id(db_path, person_id):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
            SELECT c.id, c.brand_name, c.shop, c.cost, c.img
            FROM coffee AS c
            JOIN purchase_coffee AS pc ON c.id = pc.coffee_id
            JOIN purchase_person AS pp ON pc.purchase_id = pp.purchase_id
            JOIN person AS p ON pp.person_id = p.id
            WHERE p.id = ?
            ''', (person_id,))
            rows = cursor.fetchall()
            coffees = []
            for row in rows:
                coffees.append(Coffee(row[1], row[2], row[3], row[4], row[0]))
            return coffees
    except sqlite3.Error as error:
        logger.error(error)
        raise

def get_all_coffees(db_path):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, brand_name, shop, cost, img
                FROM coffee
            ''')
            rows = cursor.fetchall()
            coffees = []
            for row in rows:
                coffees.append(Coffee(row[1], row[2], row[3], row[4], row[0]))
            return coffees
    except sqlite3.Error as error:
        logger.error(error)
        raise


def update_coffee(db_path, coffee):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE coffee
                SET brand_name = ?, shop = ?, cost = ?, img = ?
                WHERE id = ?
            ''', (coffee.brand_name, coffee.shop, coffee.cost, coffee.img, coffee.id))
            # Check if the update was successful
            if cursor.rowcount == 0:
                raise sqlite3.Error(f"No coffee found with ID {coffee.id}")

            conn.commit()
    except sqlite3.Error as error:
        logger.error(error)
        raise

def delete_coffee_by_id(db_path, coffee_id):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM coffee WHERE id = ?
            ''', (coffee_id,))
            conn.commit()
    except sqlite3.Error as error:
        logger.error(error)
        raise