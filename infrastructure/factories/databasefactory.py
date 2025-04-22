from configuration.settings import db_type, db_path
from infrastructure.database.SQLite_database import SQLiteDatabase


class DatabaseFactory:
    @staticmethod
    def create_database():
        if db_type == 'sqlite':
            db = SQLiteDatabase(db_path)
            db.init_db()
            return db
        else:
            raise ValueError(f"Unsupported database type: {db_type}")