import os
import sqlite3
import unittest
from datetime import datetime



from infrastructure.factories.database_factory import DatabaseFactory
from infrastructure.repositories.SQLite_person_repository import SQLitePersonRepository
from infrastructure.repositories.SQLite_product_repository import SQLiteProductRepository
from infrastructure.repositories.SQLite_purchase_repository import SQLitePurchaseRepository
from module.model.person import Person
from module.model.product import Product
from module.model.purchase import Purchase
from module.model.structs.name import Name



class TestRepositoryIntegration(unittest.TestCase):
    def setUp(self):
        self.db_path = 'test_repository.db'
        self.db = DatabaseFactory.create_test_database(self.db_path)
        self.person_repo = SQLitePersonRepository(self.db_path)
        self.product_repo = SQLiteProductRepository(self.db_path)
        self.purchase_repo = SQLitePurchaseRepository(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_full_integration(self):
        # Insert Person
        person = Person(Name("Alice", "Smith", ""), 3, True, "avatar.jpg")
        person.id = self.person_repo.add(person)
        retrieved_person = self.person_repo.get_by_id(person.id)
        self.assertEqual(retrieved_person.name.first_name, "Alice")

        # Insert Product
        product = Product("Brand", "Shop", 100, "product.jpg")
        product.id = self.product_repo.add(product)
        retrieved_product = self.product_repo.get_by_id(product.id)
        self.assertEqual(retrieved_product.brand_name, "Brand")

        # Insert Purchase
        purchase = Purchase("Test Purchase", [person], [product], datetime.now())
        purchase.id = self.purchase_repo.add(purchase)
        retrieved_purchase = self.purchase_repo.get_by_id(purchase.id)
        self.assertEqual(retrieved_purchase.name, "Test Purchase")
        self.assertEqual(len(retrieved_purchase.persons), 1)
        self.assertEqual(len(retrieved_purchase.products), 1)

    def test_insert_with_invalid_relationships(self):
        person = Person(Name("Invalid", "Person", ""), 3, True, "avatar.jpg")
        product = Product("Invalid", "Shop", 100, "product.jpg")
        person.id = 9999  # Non-existent ID
        product.id = 9999  # Non-existent ID
        purchase = Purchase("Invalid Purchase", [person], [product], datetime.now())
        with self.assertRaises(sqlite3.Error):
            self.purchase_repo.add(purchase)


    def test_get_persons_by_purchase_id(self):
        person = Person(Name("Alice", "Smith", ""), 3, True, "avatar.jpg")
        product = Product("Brand", "Shop", 100, "product.jpg")
        person.id = self.person_repo.add(person)
        product.id = self.product_repo.add(product)
        purchase = Purchase("Test Purchase", [person], [product], datetime.now())
        purchase.id = self.purchase_repo.add(purchase)

        persons = self.person_repo.get_by_other_id(purchase.id)
        self.assertEqual(len(persons), 1)
        self.assertEqual(persons[0].name.first_name, "Alice")

    def test_get_products_by_person_id(self):
        person = Person(Name("Bob", "Jones", ""), 3, True, "avatar.jpg")
        product = Product("Brand", "Shop", 100, "product.jpg")
        person.id = self.person_repo.add(person)
        product.id = self.product_repo.add(product)
        purchase = Purchase("Test Purchase", [person], [product], datetime.now())
        purchase.id = self.purchase_repo.add(purchase)

        products = self.product_repo.get_by_other_id(person.id)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0].brand_name, "Brand")

    def test_get_purchases_by_person_id(self):
        person = Person(Name("Charlie", "Brown", ""), 3, True, "avatar.jpg")
        product = Product("Brand", "Shop", 100, "product.jpg")
        person.id = self.person_repo.add(person)
        product.id = self.product_repo.add(product)
        purchase = Purchase("Test Purchase", [person], [product], datetime.now())
        purchase.id = self.purchase_repo.add(purchase)

        purchases = self.purchase_repo.get_by_other_id(person.id)
        self.assertEqual(len(purchases), 1)
        self.assertEqual(purchases[0].name, "Test Purchase")


if __name__ == '__main__':
    unittest.main()
