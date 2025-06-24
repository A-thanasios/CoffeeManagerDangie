import gc
import time
import os
import unittest

from Configuration.settings import test_db_path
from Infrastructure.database.SQlite.operations.SQLite_product_operations import (
    insert_product, select_product_by_id, update_product, select_all_products
)

from Infrastructure.factories.database_factory import DatabaseFactory
from MVP_DEPRECATED.Module.Model.product import Product


class TestProductOperations(unittest.TestCase):
    def setUp(self):
        self.db_path = test_db_path
        self.db = DatabaseFactory.create_test_database()
        self.valid_product = Product("Starbucks", "Main Street", 100)

    def tearDown(self):
        # enforce garbage collection
        gc.collect()
        # latency
        time.sleep(0.1)

        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_product_crud_operations(self):
        # Create & Read
        product_id = insert_product(self.db_path, self.valid_product)
        retrieved_product = select_product_by_id(self.db_path, product_id)
        self.assertIsNotNone(retrieved_product)
        self.assertEqual(retrieved_product.brand_name, "Starbucks")
        self.assertEqual(retrieved_product.cost, 100)

        # Update
        retrieved_product.cost = 120
        update_product(self.db_path, retrieved_product)
        updated_product = select_product_by_id(self.db_path, product_id)
        self.assertEqual(updated_product.cost, 120)


    def test_get_all_products(self):
        # Insert multiple products
        products = [
            Product("Brand1", "Shop1", 50),
            Product("Brand2", "Shop2", 75)
        ]
        for product in products:
            insert_product(self.db_path, product, 5)

        # Retrieve all products
        retrieved_products = select_all_products(self.db_path)
        self.assertEqual(len(retrieved_products), 2)

if __name__ == '__main__':
    unittest.main()
