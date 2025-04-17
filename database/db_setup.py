import os
import sqlite3
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(db_path: str):
    try:
        os.umask(0)
        with sqlite3.connect(db_path) as conn:
            logger.info("Connecting to database...")
            conn.execute('PRAGMA journal_mode=WAL')
            cursor = conn.cursor()
            # Enable foreign key constraints
            cursor.execute('PRAGMA foreign_keys = ON;')
            logger.info("Creating tables...")

            # Create tables
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
                    is_buying BOOLEAN NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS purchase (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    date DATE NOT NULL,
                    coffee_id INTEGER,
                    person_id INTEGER,
                    FOREIGN KEY (coffee_id) REFERENCES coffee (id),
                    FOREIGN KEY (person_id) REFERENCES person (id)
                )
            ''')

            # Commit changes
            conn.commit()
            cursor.close()
            logger.info("Database initialized successfully.")
    except sqlite3.Error as error:
        logger.error(error)
        raise