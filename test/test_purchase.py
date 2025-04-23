import unittest
from datetime import datetime

from module.data.product import Product
from module.data.person import Person
from module.data.purchase import Purchase
from module.data.structs.name import Name


class TestPurchase(unittest.TestCase):
    def setUp(self):
        self.product1 = Product("Starbucks", "Main Street", 20)
        self.product2 = Product("Costa", "Side Street", 15)
        self.person1 = Person(Name("Alice", "Wonderland"), 3)
        self.person2 = Person(Name("Bob", "La Blob"), 2)
        self.date = datetime.now()

    def test_create_purchase_with_valid_data(self):
        purchase = Purchase('purchase', [self.person1], [self.product1], self.date, 1)
        self.assertEqual(purchase.id, 1)
        self.assertEqual(purchase.name, 'purchase')
        self.assertEqual(purchase.persons, [self.person1])
        self.assertEqual(purchase.products, [self.product1])
        self.assertEqual(purchase.date, self.date)

    def test_purchase_with_multiple_persons(self):
        purchase = Purchase('group_purchase', [self.person1, self.person2], [self.product1], self.date)
        self.assertEqual(len(purchase.persons), 2)
        self.assertIn(self.person1, purchase.persons)
        self.assertIn(self.person2, purchase.persons)

    def test_purchase_with_multiple_products(self):
        purchase = Purchase('multi_product', [self.person1], [self.product1, self.product2], self.date)
        self.assertEqual(len(purchase.products), 2)
        self.assertIn(self.product1, purchase.products)
        self.assertIn(self.product2, purchase.products)

    def test_invalid_id_setter(self):
        purchase = Purchase('test', [self.person1], [self.product1], self.date)
        with self.assertRaises(ValueError):
            purchase.id = -1
        with self.assertRaises(ValueError):
            purchase.id = "invalid"

    def test_string_representation(self):
        purchase = Purchase('test', [self.person1], [self.product1], self.date, 1)
        str_repr = str(purchase)
        self.assertIn('test', str_repr)
        self.assertIn('1', str_repr)

    def test_empty_persons_list(self):
        with self.assertRaises(ValueError):
            Purchase('empty', [], [self.product1], self.date)

    def test_empty_products_list(self):
        purchase = Purchase('empty', [self.person1], [], self.date)
        self.assertEqual(len(purchase.products), 0)

    def test_date_modification(self):
        purchase = Purchase('date_test', [self.person1], [self.product1], self.date)
        new_date = datetime(2024, 1, 1)
        purchase.date = new_date
        self.assertEqual(purchase.date, new_date)


if __name__ == '__main__':
    unittest.main()