import sqlite3

from MVP.Module import Person
from MVP.Module import PersonDetail
from MVP.Module.interfaces import PersonOperations


class SQLitePersonOperations(PersonOperations):
    def insert_person(self, db_path: str, person: Person) -> int:
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()

                # Create a person instance for reference
                cursor.execute('INSERT INTO person DEFAULT VALUES')
                person.id = cursor.lastrowid

                # Insert into a person_detail table
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

                return person.id

        except sqlite3.Error as error:
            raise sqlite3.Error (error)

    def get_person_by_id(self, db_path: str, person_id: int) -> Person | None | sqlite3.Error:
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()

                cursor.execute(
                    self.__get_person_query() + 'WHERE p.id = ?',
        (person_id,))
                row = cursor.fetchone()
                if row:
                    return self.__create_person(row)
                return None

        except sqlite3.Error as error:
            return sqlite3.Error (error)


    def get_persons_by_purchase_id(self, db_path: str, purchase_id: int) -> list[Person] | None | sqlite3.Error:
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    self.__get_person_query() +
                '''
                    JOIN purchase_settlement AS ps ON p.id = ps.person_id
                    WHERE ps.purchase_id = ?
                ''', (purchase_id,))

                rows = cursor.fetchall()
                if rows:
                    return self.__create_persons_list(rows)
                return None

        except sqlite3.Error as error:
            return sqlite3.Error (error)

    def get_all_persons(self, db_path: str) -> list[Person] | None | sqlite3.Error:
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(self.__get_person_query())

                rows = cursor.fetchall()
                if rows:
                    conn.commit()
                    cursor.close()
                    return self.__create_persons_list(rows)
                return None



        except sqlite3.Error as error:
            return sqlite3.Error (error)

    def update_person(self, db_path: str, person: Person) -> bool | sqlite3.Error:
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
                    return sqlite3.Error(f"No person found with ID {person.id}")

                conn.commit()

                return True
        except sqlite3.Error as error:
            return sqlite3.Error (error)

    def delete_person_by_id(self, db_path: str, person_id: int) -> bool | sqlite3.Error:
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    DELETE FROM person WHERE id = ?
                ''', (person_id,))
                conn.commit()
                return True
        except sqlite3.Error as error:
            return sqlite3.Error (error)

    @staticmethod
    def __get_person_query() -> str:
        return '''
               SELECT   p.id,
                        d.name,
                        d.days_per_week,
                        d.is_buying,
                        d.e_mail
    
                FROM person AS p
                
                JOIN person_detail AS d 
                     ON p.id = d.person_id
                '''




    @staticmethod
    def __create_person(row):
        person_id = row[0]
        name = row[1]
        days_per_week = row[2]
        is_buying = bool(row[3])
        email = row[4]
        person_detail = PersonDetail(name, email, days_per_week, is_buying)
        person = Person(person_detail, person_id)
        return person

    def __create_persons_list(self, rows):
        persons = []
        for row in rows:
            persons.append(self.__create_person(row))
        return persons


