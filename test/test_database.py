import os
import sqlite3
import unittest
from datetime import datetime
from infrastructure.database.SQLite_database import init_db
from infrastructure.database.operations.db_coffee_operations import insert_coffee, get_coffee_by_id, update_coffee, delete_coffee
from infrastructure.database.operations.db_person_operations import insert_person, get_person_by_id, update_person, delete_person
from infrastructure.database.operations.db_purchase_operations import insert_purchase, get_purchase_by_id, update_purchase, \
    delete_purchase
from module.data.coffee import Coffee
from module.data.person import Person
from module.data.purchase import Purchase
from module.data.structs.name import Name


class TestDatabaseOperations(unittest.TestCase):
    def setUp(self):
        self.db_path = 'test_database.db'
        init_db(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    # Coffee Operations Tests
    def test_coffee_crud(self):
        # Create & Read
        coffee = Coffee("Starbucks", "Main Street", 100, "image.jpg")
        coffee_id = insert_coffee(self.db_path, coffee)
        retrieved_coffee = get_coffee_by_id(self.db_path, coffee_id)
        self.assertEqual(retrieved_coffee.brand_name, coffee.brand_name)

        # Update
        retrieved_coffee.cost = 120
        retrieved_coffee.shop = "New Location"
        update_coffee(self.db_path, retrieved_coffee)
        updated_coffee = get_coffee_by_id(self.db_path, coffee_id)
        self.assertEqual(updated_coffee.cost, 120)
        self.assertEqual(updated_coffee.shop, "New Location")

        # Delete
        delete_coffee(self.db_path, coffee_id)
        self.assertIsNone(get_coffee_by_id(self.db_path, coffee_id))

    # Person Operations Tests
    def test_person_crud(self):
        # Create & Read
        person = Person(Name("John", "M", "Doe"), 3, True, "avatar.jpg")
        person_id = insert_person(self.db_path, person)
        retrieved_person = get_person_by_id(self.db_path, person_id)
        self.assertEqual(retrieved_person.name.first_name, person.name.first_name)

        # Update
        retrieved_person.days_per_week = 4
        retrieved_person.is_buying = False
        update_person(self.db_path, retrieved_person)
        updated_person = get_person_by_id(self.db_path, person_id)
        self.assertEqual(updated_person.days_per_week, 4)
        self.assertEqual(updated_person.is_buying, False)

        # Delete
        delete_person(self.db_path, person_id)
        self.assertIsNone(get_person_by_id(self.db_path, person_id))

    # Purchase Operations Tests
    def test_purchase_crud(self):
        # Setup
        person = Person(Name("Buyer", "", "One"), 3, True, "avatar.jpg")
        coffee = Coffee("Lavazza", "Coffee Shop", 120, "coffee.jpg")
        person.id = insert_person(self.db_path, person)
        coffee.id = insert_coffee(self.db_path, coffee)

        # Create & Read
        purchase = Purchase("Morning Coffee", [person], [coffee], datetime.now())
        purchase_id = insert_purchase(self.db_path, purchase)
        retrieved_purchase = get_purchase_by_id(self.db_path, purchase_id)
        self.assertEqual(retrieved_purchase.name, purchase.name)

        # Update
        retrieved_purchase.name = "Afternoon Coffee"
        new_date = datetime.now()
        retrieved_purchase.date = new_date
        update_purchase(self.db_path, retrieved_purchase)
        updated_purchase = get_purchase_by_id(self.db_path, purchase_id)
        self.assertEqual(updated_purchase.name, "Afternoon Coffee")

        # Delete
        delete_purchase(self.db_path, purchase_id)
        self.assertIsNone(get_purchase_by_id(self.db_path, purchase_id))

    def test_update_with_invalid_data(self):
        coffee = Coffee("Lavazza", "Coffee Shop", 120, "coffee.jpg")

        # Test update of non-existent record
        coffee.id = 9999
        with self.assertRaises(sqlite3.Error):
            update_coffee(self.db_path, coffee)  # coffee.id is None

        # Test Person update with non-existent ID
        person = Person(Name("Test", "", "User"), 3, True, "avatar.jpg")
        person.id = 9999  # Non-existent ID
        with self.assertRaises(sqlite3.Error):
            update_person(self.db_path, person)

        # Test Purchase update with invalid relationships
        purchase = Purchase("Test Purchase", [], [], datetime.now())
        purchase.id = 9999  # Non-existent ID
        with self.assertRaises(sqlite3.Error):
            update_purchase(self.db_path, purchase)


if __name__ == '__main__':
    unittest.main()