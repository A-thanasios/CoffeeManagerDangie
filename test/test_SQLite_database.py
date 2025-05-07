import os
import sqlite3
import unittest
from datetime import datetime
from infrastructure.database.SQlite.SQLite_database import SQLiteDatabase
from infrastructure.database.SQlite.operations.SQLite_product_operations import (
    insert_product, get_product_by_id, update_product, delete_product_by_id, get_all_products
)
from infrastructure.database.SQlite.operations.SQLite_person_operations import (
    insert_person, get_person_by_id, update_person, delete_person_by_id, get_all_persons
)
from infrastructure.database.SQlite.operations.SQLite_purchase_operations import (
    insert_purchase, get_purchase_by_id, update_purchase, delete_purchase_by_id, get_all_purchases
)
from infrastructure.factories.database_factory import DatabaseFactory
from module.model.product import Product
from module.model.person import Person
from module.model.purchase import Purchase
from module.model.structs.name import Name




class TestSQLiteDatabase(unittest.TestCase):
    def setUp(self):
        self.db_path = 'test.db'
        self.db = DatabaseFactory.create_test_database(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    # Product Operations Tests
    def test_product_crud(self):
        # Create & Read
        product = Product("Starbucks", "Main Street", 100, "image.jpg")
        product_id = insert_product(self.db_path, product)
        retrieved_product = get_product_by_id(self.db_path, product_id)
        self.assertEqual(retrieved_product.brand_name, product.brand_name)

        # Update
        retrieved_product.cost = 120
        retrieved_product.shop = "New Location"
        update_product(self.db_path, retrieved_product)
        updated_product = get_product_by_id(self.db_path, product_id)
        self.assertEqual(updated_product.cost, 120)
        self.assertEqual(updated_product.shop, "New Location")

        # Delete
        delete_product_by_id(self.db_path, product_id)
        self.assertIsNone(get_product_by_id(self.db_path, product_id))

    def test_insert_product_with_invalid_data(self):
        with self.assertRaises(ValueError):
            Product(None, "Shop", 100)  # Invalid brand_name

    def test_insert_product_with_null_values(self):
        with self.assertRaises(ValueError):
            Product(None, None, 0)  # Invalid product model

    def test_get_all_products(self):
        product1 = Product("Brand1", "Shop1", 50)
        product2 = Product("Brand2", "Shop2", 75)
        insert_product(self.db_path, product1)
        insert_product(self.db_path, product2)
        products = get_all_products(self.db_path)
        self.assertEqual(len(products), 2)

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
        delete_person_by_id(self.db_path, person_id)
        self.assertIsNone(get_person_by_id(self.db_path, person_id))

    def test_insert_person_with_invalid_days(self):
        with self.assertRaises(ValueError):
            Person(Name("John", "M", "Doe"), 6)  # Invalid days_per_week

    def test_insert_person_with_invalid_name(self):
        with self.assertRaises(ValueError):
            Person(Name("", "", ""), 3)  # Invalid name

    def test_get_all_persons(self):
        person1 = Person(Name("Alice", "Smith", ""), 3)
        person2 = Person(Name("Bob", "Jones", ""), 5)
        insert_person(self.db_path, person1)
        insert_person(self.db_path, person2)
        persons = get_all_persons(self.db_path)
        self.assertEqual(len(persons), 2)

    # Purchase Operations Tests
    def test_purchase_crud(self):
        # Setup
        person = Person(Name("Buyer", "One", ""), 3, True, "avatar.jpg")
        product = Product("Lavazza", "product Shop", 120, "product.jpg")
        person.id = insert_person(self.db_path, person)
        product.id = insert_product(self.db_path, product)

        # Create & Read
        purchase = Purchase("Morning product", [person], [product], datetime.now())
        purchase_id = insert_purchase(self.db_path, purchase)
        retrieved_purchase = get_purchase_by_id(self.db_path, purchase_id)
        self.assertEqual(retrieved_purchase.name, purchase.name)

        # Update
        retrieved_purchase.name = "Afternoon product"
        new_date = datetime.now()
        retrieved_purchase.date = new_date
        update_purchase(self.db_path, retrieved_purchase)
        updated_purchase = get_purchase_by_id(self.db_path, purchase_id)
        self.assertEqual(updated_purchase.name, "Afternoon product")

        # Delete
        delete_purchase_by_id(self.db_path, purchase_id)
        self.assertIsNone(get_purchase_by_id(self.db_path, purchase_id))


    def test_get_all_purchases(self):
        person = Person(Name("Buyer", "One", ""), 3, True, "avatar.jpg")
        product = Product("Lavazza", "Shop", 120, "product.jpg")
        person.id = insert_person(self.db_path, person)
        product.id = insert_product(self.db_path, product)
        purchase1 = Purchase("Purchase1", [person], [product], datetime.now())
        purchase2 = Purchase("Purchase2", [person], [product], datetime.now())
        insert_purchase(self.db_path, purchase1)
        insert_purchase(self.db_path, purchase2)
        purchases = get_all_purchases(self.db_path)
        self.assertEqual(len(purchases), 2)

    def test_delete_nonexistent_purchase(self):
        with self.assertRaises(sqlite3.Error):
            delete_purchase_by_id(self.db_path, 9999)


    def test_update_with_invalid_data(self):
        product = Product("Lavazza", "product Shop", 120, "product.jpg")

        # Test update of non-existent record
        product.id = 9999
        with self.assertRaises(sqlite3.Error):
            update_product(self.db_path, product)  # product.id is None

        # Test Person update with non-existent ID
        person = Person(Name("Test", "User", ""), 3, True, "avatar.jpg")
        person.id = 9999  # Non-existent ID
        with self.assertRaises(sqlite3.Error):
            update_person(self.db_path, person)




if __name__ == '__main__':
    unittest.main()
