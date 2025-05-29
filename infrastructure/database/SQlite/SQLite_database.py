import os
import sqlite3

from Module.interfaces import Database



class SQLiteDatabase(Database):
    def __init__(self, path):
        if not path:
            raise ValueError("Database path cannot be empty.")
        self.__path = path

    def init_db(self):
        if self.exists():
            print("Database already exists.")
            return
    

        try:
            with sqlite3.connect(self.__path) as conn:
                cursor = conn.cursor()
                cursor.execute('PRAGMA foreign_keys = ON;')

                cursor.execute('''
                   CREATE TABLE IF NOT EXISTS person
                   (
                       id   INTEGER PRIMARY KEY
                   )
                   ''')

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS person_detail
                    (
                        id              INTEGER PRIMARY KEY,
                        person_id       INTEGER,
                        name            TEXT NOT NULL CHECK (length(name) > 0),
                        e_mail          TEXT CHECK (e_mail LIKE '%_@_%._%'),
                        days_per_week   INTEGER NOT NULL CHECK (days_per_week >= 0 AND days_per_week <= 5),
                        is_buying       INTEGER NOT NULL CHECK (is_buying IN(0, 1)) DEFAULT 1,
                        
                        FOREIGN KEY (person_id) REFERENCES person (id) ON DELETE CASCADE
                    )
                    ''')

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS purchase 
                    (
                        id      INTEGER PRIMARY KEY
                        
                    )
                ''')

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS purchase_detail
                    (
                    id      INTEGER PRIMARY KEY,
                    name    TEXT NOT NULL,
                    date    DATE NOT NULL,

                    FOREIGN KEY (id) REFERENCES purchase (id) ON DELETE CASCADE
                    )           
                ''')

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS purchase_settlement
                    (
                        purchase_id INTEGER,
                        person_id   INTEGER,
                        amount      REAL NOT NULL CHECK (amount >= 0),
                        is_paid     BOOL NOT NULL DEFAULT 0,
                        
                        PRIMARY KEY (purchase_id, person_id),
                        FOREIGN KEY (purchase_id)   REFERENCES purchase (id) ON DELETE CASCADE,
                        FOREIGN KEY (person_id)     REFERENCES person (id) ON DELETE CASCADE
                    )
                ''')

                cursor.execute('''
                   CREATE TABLE IF NOT EXISTS product
                   (
                       id         INTEGER PRIMARY KEY,
                       purchase_id INTEGER NOT NULL,
                       brand_name TEXT NOT NULL CHECK (length(brand_name) > 0),
                       shop       TEXT,
                       cost       REAL NOT NULL CHECK (cost >= 0),
                       
                       FOREIGN KEY (purchase_id) REFERENCES purchase (id) ON DELETE CASCADE
                   )
                   ''')

                conn.commit()
        except sqlite3.Error as error:
            self.__path = ''
            raise Exception(f"Error initializing database: {error}")


    def exists(self):
        return os.path.exists(self.__path)

    @property
    def path(self):
        return self.__path
    
    @property
    def type(self):
        return "sqlite"