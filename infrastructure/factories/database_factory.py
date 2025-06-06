from configuration.settings import db_type, db_path

from module.interfaces.database import Database
from infrastructure.database.SQlite.SQLite_database import SQLiteDatabase



class DatabaseFactory:
    @staticmethod
    def create_database() -> Database:
        if db_type == 'sqlite':
            db = SQLiteDatabase(db_path)
            db.init_db()
            return db
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

    @staticmethod
    def create_test_database(path='test_database.db') -> Database:
        if db_type == 'sqlite':
            db = SQLiteDatabase(path)
            db.init_db()
            return db
        else:
            raise ValueError(f"Unsupported database type: {db_type}")