import os
import unittest
from unittest.mock import patch, MagicMock
from infrastructure.factories.database_factory import DatabaseFactory
from infrastructure.database.SQlite.SQLite_database import SQLiteDatabase


class TestDatabaseFactory(unittest.TestCase):
    def setUp(self):
        self.test_db_path = 'test_database.db'
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def tearDown(self):
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    @patch('infrastructure.factories.database_factory.db_type', 'sqlite')
    @patch('infrastructure.factories.database_factory.db_path', 'test_database.db')
    def test_create_sqlite_database(self):
        db = DatabaseFactory.create_database()
        self.assertIsInstance(db, SQLiteDatabase)
        self.assertEqual(db.path, 'test_database.db')

    @patch('infrastructure.factories.database_factory.db_type', 'unsupported_db')
    def test_create_unsupported_database(self):
        with self.assertRaises(ValueError) as context:
            DatabaseFactory.create_database()
        self.assertIn("Unsupported database type: unsupported_db", str(context.exception))

    @patch('infrastructure.factories.database_factory.SQLiteDatabase')
    @patch('infrastructure.factories.database_factory.db_type', 'sqlite')
    @patch('infrastructure.factories.database_factory.db_path', 'test_database.db')
    def test_sqlite_database_initialization(self, mock_sqlite_database):
        mock_instance = MagicMock()
        mock_sqlite_database.return_value = mock_instance

        db = DatabaseFactory.create_database()

        mock_sqlite_database.assert_called_once_with('test_database.db')
        mock_instance.init_db.assert_called_once()
        self.assertEqual(db, mock_instance)


if __name__ == '__main__':
    unittest.main()
