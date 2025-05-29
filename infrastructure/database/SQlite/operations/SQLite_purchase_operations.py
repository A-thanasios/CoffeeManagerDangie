import sqlite3
from datetime import datetime

from Module import Purchase
from Module.model.data.purchase_detail import PurchaseDetail

from infrastructure.database.SQlite.operations.SQLite_product_operations import get_product_by_id, insert_product, \
    get_products_by_purchase_id
from infrastructure.database.SQlite.operations.SQLite_person_operations import get_person_by_id, \
    get_persons_by_purchase_id


def insert_purchase(db_path, purchase):
    try:
        with (sqlite3.connect(db_path) as conn):
            conn.execute("PRAGMA foreign_keys = ON")
            cursor = conn.cursor()


            cursor.execute('INSERT INTO purchase DEFAULT VALUES')
            purchase_id = cursor.lastrowid

            cursor.execute(
                '''
                INSERT INTO purchase_detail 
                    (
                        purchase_id,
                        name,
                        date
                    )
                VALUES (?, ?, datetime(?))
                ''',
                (
                purchase_id,
                purchase.name,
                purchase.date.isoformat()
            ))

            # Insert relationships with persons

            settlement_values = [
                (purchase_id, settlement.person.id, settlement.amount, settlement.is_paid)
                for settlement in purchase.purchase_settlements
            ]

            cursor.executemany(
                '''
                INSERT INTO purchase_settlement 
                    (
                        purchase_id,
                        person_id,
                        amount,
                        is_paid
                    )
                ''',
                settlement_values
            )

            conn.commit()

            # Insert products that are part of the purchase
            for product in purchase.products:
                insert_product(db_path, product, purchase_id)

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
                SELECT 
                    name,
                    date,
                from purchase_detail as pd
                WHERE purchase_id = ?
                '''), purchase_id
            detail = cursor.fetchone()

            # get purchase_settlements
            cursor.executemany(
                '''
                SELECT
                    person_id,
                    amount,
                    is_paid
                FROM purchase_settlement
                WHERE purchase_id = ?
                ''', purchase_id
            )
            settlements = cursor.fetchall()

            # get persons
            persons = get_persons_by_purchase_id(db_path, purchase_id)

            # get products
            products = get_products_by_purchase_id(db_path, purchase_id)

            return __create_purchase(purchase_id, detail, persons, products, settlements)

    except sqlite3.Error as error:
        raise sqlite3.Error (error)


def get_purchases_by_person_id(db_path, person_id):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            cursor.execute('''
                SELECT id
                FROM purchase_settlements
                WHERE person_id = ?
            ''', (person_id,))
            rows = cursor.fetchall()

            purchases = []
            for row in rows:
                purchases.append(get_purchase_by_id(db_path, purchase_id=row[0]))

            return purchases
    except sqlite3.Error as error:
        raise sqlite3.Error(error)

def get_all_purchases(db_path):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id
                FROM purchase
            ''')
            rows = cursor.fetchall()
            purchases = []
            for row in rows:
                purchases.append(get_purchase_by_id(db_path, purchase_id=row[0]))
            return purchases

    except sqlite3.Error as error:
        raise sqlite3.Error (error)

def update_purchase(db_path, purchase):
    raise Exception('Not implemented')

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

def __create_purchase(purchase_id, detail, persons, products, settlements):
    # Convert date to datetime object
    purchase_date = datetime.strptime(detail[2], "%Y-%m-%d %H:%M:%S")
    detail = PurchaseDetail(detail[1], purchase_date)

    return Purchase(detail, persons, products, settlements, purchase_id)
