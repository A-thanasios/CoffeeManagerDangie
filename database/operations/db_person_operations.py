import sqlite3

from database.db_setup import logger
from src.data.person import Person
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

def delete_person(db_path, person_id):
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