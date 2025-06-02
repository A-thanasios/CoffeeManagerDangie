import os
import sqlite3
import unittest

from Configuration.settings import test_db_path
from Infrastructure.database.SQlite.SQLite_database import SQLiteDatabase
from Infrastructure.factories.database_factory import DatabaseFactory

class TestDatabaseLifecycle(unittest.TestCase):
    def setUp(self):
        self.db_path = test_db_path

    def tearDown(self):
        # Clean up the database file after each test
        if os.path.exists(self.db_path):
            os.remove(self.db_path)



    def test_database_creation(self):
        # Test database creation
        db = DatabaseFactory.create_test_database()
        db.init_db()
        self.assertTrue(os.path.exists(self.db_path))

        # Verify tables existence
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        expected_tables = [
            'person',
            'person_detail',
            'purchase',
            'purchase_detail',
            'purchase_settlement',
            'product'
        ]

        for expected_table in expected_tables:
            self.assertIn(expected_table, table_names,
                          f"Expected table '{expected_table}' not found in the database.")


        # Verify table structure
        expected_person_columns = ['id']
        expected_person_detail_columns = ['id', 'person_id', 'name', 'e_mail', 'days_per_week', 'is_buying']
        expected_purchase_columns = ['id']
        expected_purchase_detail_columns = ['id', 'name', 'date']
        expected_purchase_settlement_columns = ['purchase_id', 'person_id', 'amount', 'is_paid']
        expected_product_columns = ['id', 'purchase_id', 'brand_name', 'shop', 'cost']

        cursor.execute("PRAGMA table_info(person)")
        person_columns = [column[1] for column in cursor.fetchall()]
        for col in person_columns:
            self.assertIn(col, expected_person_columns,
                          f"Column '{col}' not found in 'person' table.")

        cursor.execute("PRAGMA table_info(person_detail)")
        person_detail_columns = [column[1] for column in cursor.fetchall()]
        for col in person_detail_columns:
            self.assertIn(col, expected_person_detail_columns,
                          f"Column '{col}' not found in 'person_detail' table.")
        cursor.execute("PRAGMA table_info(purchase)")
        purchase_columns = [column[1] for column in cursor.fetchall()]
        for col in purchase_columns:
            self.assertIn(col, expected_purchase_columns,
                          f"Column '{col}' not found in 'purchase' table.")

        cursor.execute("PRAGMA table_info(purchase_detail)")
        purchase_detail_columns = [column[1] for column in cursor.fetchall()]
        for col in purchase_detail_columns:
            self.assertIn(col, expected_purchase_detail_columns,
                          f"Column '{col}' not found in 'purchase_detail' table.")
        cursor.execute("PRAGMA table_info(purchase_settlement)")
        purchase_settlement_columns = [column[1] for column in cursor.fetchall()]
        for col in purchase_settlement_columns:
            self.assertIn(col, expected_purchase_settlement_columns,
                          f"Column '{col}' not found in 'purchase_settlement' table.")


        cursor.execute("PRAGMA table_info(product)")
        product_columns = [column[1] for column in cursor.fetchall()]
        for col in product_columns:
            self.assertIn(col, expected_product_columns,
                          f"Column '{col}' not found in 'product' table.")



        conn.close()

if __name__ == '__main__':
    unittest.main()
