import unittest
from datetime import datetime

from src.data.coffee import Coffee
from src.data.person import Person
from src.data.purchase import Purchase
from src.data.structs.name import Name


class TestPurchase(unittest.TestCase):
    def setUp(self):
        self.coffee = Coffee("Starbucks", "Main Street", 20)
        self.person = Person(Name("Alice", "Wonderland"), 3)
        self.person2 = Person(Name("Bob", "La Blob"), 2)
        self.date = datetime.now()

    def test_allows_valid_persons(self):
        coffee = self.coffee
        coffee.cost = 5
        purchase = Purchase('purchase',[self.person, self.person2], coffee, datetime.now())
        self.assertEqual(purchase.persons, [self.person, self.person2])

    def test_allows_valid_date(self):
        coffee = Coffee("Starbucks", "Main Street", 5)
        purchase = Purchase('purchase', [self.person], coffee, datetime.now())
        new_date = datetime(2023, 1, 1)
        purchase.date = new_date
        self.assertEqual(purchase.date, new_date)


if __name__ == "__main__":
    unittest.main()