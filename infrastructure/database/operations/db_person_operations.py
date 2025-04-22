import sqlite3

from infrastructure.database.SQLite_database import logger
from module.data.person import Person
from module.data.structs.name import Name


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
            person.id = new_id
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

def get_persons_by_purchase_id(db_path, purchase_id):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT p.id, p.first_name, p.middle_name, p.last_name, p.days_per_week, p.is_buying, p.img 
                FROM person AS p
                JOIN purchase_person AS pp ON p.id = pp.person_id
                WHERE pp.purchase_id = ?
            ''', (purchase_id,))
            rows = cursor.fetchall()
            persons = []
            for row in rows:
                name = Name(row[1], row[2], row[3])
                persons.append(Person(name, row[4], row[5], row[6], row[0]))
            return persons
    except sqlite3.Error as error:
        logger.error(error)
        raise

def get_all_persons(db_path):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, first_name, middle_name, last_name, days_per_week, is_buying, img 
                FROM person
            ''')
            rows = cursor.fetchall()
            persons = []
            for row in rows:
                name = Name(row[1], row[2], row[3])
                persons.append(Person(name, row[4], row[5], row[6], row[0]))
            return persons
    except sqlite3.Error as error:
        logger.error(error)
        raise

def update_person(db_path, person):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE person
                SET first_name = ?, middle_name = ?, last_name = ?, days_per_week = ?, is_buying = ?, img = ?
                WHERE id = ?
            ''', (person.name.first_name, person.name.middle_name, person.name.last_name,
                  person.days_per_week, person.is_buying, person.img, person.id))
            # Check if the update was successful
            if cursor.rowcount == 0:
                raise sqlite3.Error(f"No person found with ID {person.id}")

            conn.commit()
    except sqlite3.Error as error:
        logger.error(error)
        raise

def delete_person_by_id(db_path, person_id):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM person WHERE id = ?
            ''', (person_id,))
            conn.commit()
    except sqlite3.Error as error:
        logger.error(error)
        raise


