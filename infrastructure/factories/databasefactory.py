from configuration.settings import db_type, db_path
from infrastructure.database.SQLite_database import SQLiteDatabase


class DatabaseFactory:
    @staticmethod
    def create_database():
        if db_type == 'sqlite':
            return SQLiteDatabase(db_path)
        else:
            raise ValueError(f"Unsupported database type: {db_type}")