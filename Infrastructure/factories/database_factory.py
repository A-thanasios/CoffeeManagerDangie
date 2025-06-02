from Configuration.settings import db_type, db_path, test_db_path

from MVP.Module.interfaces import Database
from Infrastructure.database.SQlite.SQLite_database import SQLiteDatabase



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
    def create_test_database() -> Database:
        if db_type == 'sqlite':
            db = SQLiteDatabase(test_db_path)
            db.init_db()
            return db
        else:
            raise ValueError(f"Unsupported database type: {db_type}")