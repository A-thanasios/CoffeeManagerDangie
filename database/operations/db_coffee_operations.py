import sqlite3

from database.db_setup import logger
from src.data.coffee import Coffee


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