import sqlite3

from Module import Person
from Module import PersonDetail


def insert_person(db_path: str, person: Person):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Create person instance for reference
            cursor.execute('INSERT INTO person DEFAULT VALUES')
            person.id = cursor.lastrowid

            # Insert into person_detail table
            cursor.execute('''
                INSERT INTO person_detail 
                (
                    person_id,
                    name,
                    e_mail,
                    days_per_week,
                    is_buying
                )
                VALUES (?, ?, ?, ?, ?)
            ''',
(
                person.id,
                person.person_detail.name,
                person.person_detail.e_mail,
                person.person_detail.days_per_week,
                person.person_detail.is_buying
            ))
            conn.commit()
            cursor.close()
    except sqlite3.Error as error:
        raise sqlite3.Error (error)

def get_person_by_id(db_path: str, person_id: int):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            cursor.execute(
                get_person_query(),
    (person_id,))
            row = cursor.fetchone()
            if row:
                return __create_person(row)
            return None

    except sqlite3.Error as error:
        raise sqlite3.Error (error)


def get_persons_by_purchase_id(db_path: str, purchase_id: int):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                get_person_query() +
            '''
                JOIN purchase_person AS pp ON p.id = pp.person_id
                WHERE pp.purchase_id = ?
            ''', (purchase_id,))

            rows = cursor.fetchall()
            if rows:
                return __create_persons_list(rows)
            return None

    except sqlite3.Error as error:
        raise sqlite3.Error (error)

def get_all_persons(db_path: str):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(get_person_query())

            rows = cursor.fetchall()
            if rows:
                return __create_persons_list(rows)
            return None

    except sqlite3.Error as error:
        raise sqlite3.Error (error)

def update_person(db_path: str, person: Person):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE person_detail
                SET name = ?, 
                    e_mail = ?, 
                    days_per_week = ?, 
                    is_buying = ?
                WHERE id = ?
            ''', (
                    person.person_detail.name,
                    person.person_detail.e_mail,
                    person.person_detail.days_per_week,
                    person.person_detail.is_buying,
                    person.id))
            # Check if the update was successful
            if cursor.rowcount == 0:
                raise sqlite3.Error(f"No person found with ID {person.id}")

            conn.commit()
    except sqlite3.Error as error:
        raise sqlite3.Error (error)

def delete_person_by_id(db_path: str, person_id: int):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                DELETE FROM person WHERE id = ?
            ''', (person_id,))
            conn.commit()
    except sqlite3.Error as error:
        raise sqlite3.Error (error)

def get_person_query():
    return '''
           SELECT   p.id,
                    d.name,
                    d.days_per_week,
                    d.is_buying,
                    d.e_mail

            FROM person AS p
            
            JOIN person_detail AS d 
                 ON p.id = d.person_id

            WHERE p.id = ?
           '''


def __create_person(row):
    person_id = row[0]
    name = row[1]
    days_per_week = row[2]
    is_buying = bool(row[3])
    email = row[4]
    person_detail = PersonDetail(name, email, days_per_week, is_buying)
    person = Person(person_detail, person_id)
    return person

def __create_persons_list(rows):
    persons = []
    for row in rows:
        persons.append(__create_person(row))
    return persons


