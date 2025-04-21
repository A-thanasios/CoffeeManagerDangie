import os
import sqlite3
import logging

db_path = os.path.join('infrastructure/database', 'coffee_manager.db')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db():
    try:
        with sqlite3.connect(db_path) as conn:
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
    except sqlite3.Error as error:
        logger.error(error)
        raise

def db_exists():
    return os.path.exists(db_path)