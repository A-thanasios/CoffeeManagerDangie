import os
import sqlite3
import logging



# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SQLiteDatabase:
    def __init__(self, path):
        if not path:
            raise ValueError("Database path cannot be empty.")
        self.__path = path

    def init_db(self):
        if self.db_exists():
            logger.info(f"Database already exists at {self.__path}.")
            return

        try:
            logger.info(f"Creating database at {self.db_path}.")
            with sqlite3.connect(self.__path) as conn:
                cursor = conn.cursor()
                cursor.execute('PRAGMA foreign_keys = ON;')

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS coffee (
                        id INTEGER PRIMARY KEY,
                        brand_name TEXT NOT NULL,
                        shop TEXT,
                        cost REAL NOT NULL,
                        img TEXT
                    )
                ''')

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS person (
                        id INTEGER PRIMARY KEY,
                        first_name TEXT NOT NULL,
                        middle_name TEXT,
                        last_name TEXT NOT NULL,
                        days_per_week INTEGER NOT NULL,
                        is_buying BOOLEAN NOT NULL,
                        img TEXT
                    )
                ''')

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS purchase (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        date DATE NOT NULL
                    )
                ''')

                # M:N Tables
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS purchase_person (
                        purchase_id INTEGER,
                        person_id INTEGER,
                        PRIMARY KEY (purchase_id, person_id),
                        FOREIGN KEY (purchase_id) REFERENCES purchase (id),
                        FOREIGN KEY (person_id) REFERENCES person (id)
                    )
                ''')

                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS purchase_coffee (
                        purchase_id INTEGER,
                        coffee_id INTEGER,
                        quantity INTEGER NOT NULL DEFAULT 1,
                        PRIMARY KEY (purchase_id, coffee_id),
                        FOREIGN KEY (purchase_id) REFERENCES purchase (id),
                        FOREIGN KEY (coffee_id) REFERENCES coffee (id)
                    )
                ''')

                conn.commit()
                logger.info(f"Database created at {self.__path}.")
        except sqlite3.Error as error:
            logger.error(error)
            db_path = ''
            raise

    def exists(self):
        return os.path.exists(self.__path)

    @property
    def path(self):
        return self.__path
