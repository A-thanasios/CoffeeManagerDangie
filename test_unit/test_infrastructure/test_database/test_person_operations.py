import gc
import os
import unittest
import time
from datetime import datetime

from Configuration.settings import test_db_path
from Infrastructure.database.SQlite.operations.SQLite_person_operations import SQLitePersonOperations
from Infrastructure.database.SQlite.operations.SQLite_purchase_operations import insert_purchase
from Infrastructure.factories.database_factory import DatabaseFactory
from MVP.Module import Person, PersonDetail, PurchaseDetail, PurchaseSettlement, Purchase, Product


class TestPersonOperations(unittest.TestCase):
    def setUp(self):
        self.db_path = test_db_path
        self.db = DatabaseFactory.create_test_database()
        self.person_operations = SQLitePersonOperations()
        self.valid_person_detail = PersonDetail("John", "john@test.com", 3)
        self.valid_person_detail2 = PersonDetail("Jolie", "jojo@daf.eu", 5)
        self.valid_person = Person(self.valid_person_detail)
        self.valid_person2 = Person(self.valid_person_detail2)

    def tearDown(self):
        # enforce garbage collection
        gc.collect()
        # latency
        time.sleep(0.1)

        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_person_crud_operations(self):
        # Create & Read
        person_id = self.person_operations.insert_person(self.db_path, self.valid_person)
        retrieved_person = self.person_operations.get_person_by_id(self.db_path, person_id)
        self.assertIsNotNone(retrieved_person)
        self.assertEqual(retrieved_person.person_detail.name, self.valid_person.person_detail.name)
        self.assertEqual(retrieved_person.person_detail.e_mail, "john@test.com")

        # Update
        retrieved_person.person_detail.days_per_week = 4
        self.person_operations.update_person(self.db_path, retrieved_person)
        updated_person = self.person_operations.get_person_by_id(self.db_path, person_id)
        self.assertEqual(updated_person.person_detail.days_per_week, 4)

    def test_get_person_by_purchase_id(self):


        # Insert a person related to the purchase
        person_id = self.person_operations.insert_person(self.db_path, self.valid_person)

        # Create a purchase and insert it into the database
        purchase_detail = PurchaseDetail("Test Purchase", datetime.now())
        purchase_settlement = PurchaseSettlement(self.valid_person, 100)
        product = Product("Test Product", "test_shop", 100)
        purchase = Purchase(purchase_detail,
                            [self.valid_person], [product],
                            [purchase_settlement], )
        purchase_id = insert_purchase(self.db_path, purchase)

        # Retrieve persons by purchase ID
        persons = self.person_operations.get_persons_by_purchase_id(self.db_path, purchase_id)
        self.assertIsNotNone(persons)
        self.assertGreater(len(persons), 0)
        self.assertEqual(persons[0].id, person_id)

    def test_get_all_persons(self):
        # Insert multiple persons
        persons = [
            self.valid_person,
            self.valid_person2
        ]
        persons_id = []
        for person in persons:
            persons_id.append(self.person_operations.insert_person(self.db_path, person))

        # Retrieve all persons
        retrieved_persons = self.person_operations.get_all_persons(self.db_path)
        retrieved_persons_ids = [p.id for p in retrieved_persons]
        self.assertIn(persons_id[0], retrieved_persons_ids)

    def test_cascade_delete(self):
        # Create a person and related purchase
        person_id = self.person_operations.insert_person(self.db_path, self.valid_person)
        person2_id = self.person_operations.insert_person(self.db_path, self.valid_person2)
        person2 = self.person_operations.get_person_by_id(self.db_path, person2_id)


        # Delete a person
        self.person_operations.delete_person_by_id(self.db_path, person_id)

        # Verify a person is deleted
        deleted_person = self.person_operations.get_person_by_id(self.db_path, person_id)
        self.assertIsNone(deleted_person)

        # Verify person's detail is deleted
        deleted_person_detail = self.person_operations.get_person_by_id(self.db_path, person_id)
        self.assertIsNone(deleted_person_detail)

        # Verify the other person is still there
        other_person = self.person_operations.get_person_by_id(self.db_path, person2_id)
        self.assertIsNotNone(other_person)
        self.assertEqual(other_person.person_detail.name, person2.person_detail.name)



if __name__ == '__main__':
    unittest.main()
