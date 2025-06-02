import gc
import os
import time
import unittest
from datetime import datetime

from Configuration.settings import test_db_path
from Infrastructure.database.SQlite.operations.SQLite_purchase_operations import (
    insert_purchase, get_purchase_by_id, delete_purchase_by_id, get_all_purchases
)
from Infrastructure.database.SQlite.operations.SQLite_person_operations import PersonOperations
from Infrastructure.database.SQlite.operations.SQLite_product_operations import get_product_by_id

from Infrastructure.factories.database_factory import DatabaseFactory
from MVP.Module import Purchase, PurchaseDetail, PurchaseSettlement, Person, PersonDetail, Product

class TestPurchaseOperations(unittest.TestCase):
    def setUp(self):
        self.db_path = test_db_path
        self.db = DatabaseFactory.create_test_database()
        self.person_operations = PersonOperations()

        # Test data setup
        self.product = Product("Lavazza", "Coffee Shop", 120)
        self.person_id = self.person_operations.insert_person(self.db_path, Person(PersonDetail("Buyer", "buyer@test.com", 3)))
        self.person = self.person_operations.get_person_by_id(self.db_path, self.person_id)
        self.person2_id = self.person_operations.insert_person(self.db_path, Person(PersonDetail("Second", "second@test.com", 4)))
        self.person2 = self.person_operations.get_person_by_id(self.db_path, self.person2_id)
        self.product2 = Product("Illy", "Coffee Shop", 150)




        self.purchase_detail = PurchaseDetail("Morning Coffee", datetime.now())
        self.settlement = PurchaseSettlement(self.person, 120)
        self.settlement2 = PurchaseSettlement(self.person2, 150)
        self.purchase = Purchase(
            self.purchase_detail,
            [self.person],
            [self.product],
            [self.settlement]
        )

    def tearDown(self):
        # enforce garbage collection
        gc.collect()
        # latency
        time.sleep(0.1)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_purchase_crud_operations(self):
        # Create & Read
        purchase_id = insert_purchase(self.db_path, self.purchase)
        retrieved_purchase = get_purchase_by_id(self.db_path, purchase_id)

        self.assertIsNotNone(retrieved_purchase)
        self.assertEqual(retrieved_purchase.purchase_detail.name, "Morning Coffee")
        self.assertEqual(len(retrieved_purchase.persons), 1)
        self.assertEqual(len(retrieved_purchase.products), 1)
        self.assertEqual(len(retrieved_purchase.purchase_settlements), 1)

    def test_purchase_relationships(self):
        # case with multiple persons and products

        complex_purchase = Purchase(
            PurchaseDetail("Group Coffee", datetime.now()),
            [self.person, self.person2],
            [self.product, self.product2],
            [self.settlement, self.settlement2]
        )

        purchase_id = insert_purchase(self.db_path, complex_purchase)
        retrieved_purchase = get_purchase_by_id(self.db_path, purchase_id)

        self.assertEqual(len(retrieved_purchase.persons), 2)
        self.assertEqual(len(retrieved_purchase.products), 2)
        self.assertEqual(len(retrieved_purchase.purchase_settlements), 2)

    def test_cascade_delete(self):
        # create a purchase
        purchase_id = insert_purchase(self.db_path, self.purchase)

        # verify that the purchase was created
        purchase = get_purchase_by_id(self.db_path, purchase_id)
        self.assertIsNotNone(purchase)

        # delete the purchase
        delete_purchase_by_id(self.db_path, purchase_id)

        # verify that the purchase was deleted
        deleted_purchase = get_purchase_by_id(self.db_path, purchase_id)
        self.assertIsNone(deleted_purchase)

        # Verify that related persons still exist and products are deleted
        person = self.person_operations.get_person_by_id(self.db_path, self.person.id)
        product = get_product_by_id(self.db_path, self.product.id)

        self.assertIsNotNone(person)
        self.assertIsNone(product)

    def test_get_all_purchases(self):
        # create multiple purchases
        purchase1 = Purchase(
            PurchaseDetail("Purchase 1", datetime.now()),
            [self.person],
            [self.product],
            [self.settlement]
        )
        purchase2 = Purchase(
            PurchaseDetail("Purchase 2", datetime.now()),
            [self.person],
            [self.product],
            [self.settlement]
        )

        insert_purchase(self.db_path, purchase1)
        insert_purchase(self.db_path, purchase2)

        # get all purchases
        all_purchases = get_all_purchases(self.db_path)
        self.assertEqual(len(all_purchases), 2)

if __name__ == '__main__':
    unittest.main()
