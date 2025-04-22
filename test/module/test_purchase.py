import unittest
from datetime import datetime

from module.data.coffee import Coffee
from module.data.person import Person
from module.data.purchase import Purchase
from module.data.structs.name import Name


class TestPurchase(unittest.TestCase):
    def setUp(self):
        self.coffee1 = Coffee("Starbucks", "Main Street", 20)
        self.coffee2 = Coffee("Costa", "Side Street", 15)
        self.person1 = Person(Name("Alice", "Wonderland"), 3)
        self.person2 = Person(Name("Bob", "La Blob"), 2)
        self.date = datetime.now()

    def test_create_purchase_with_valid_data(self):
        purchase = Purchase('purchase', [self.person1], [self.coffee1], self.date, 1)
        self.assertEqual(purchase.id, 1)
        self.assertEqual(purchase.name, 'purchase')
        self.assertEqual(purchase.persons, [self.person1])
        self.assertEqual(purchase.coffees, [self.coffee1])
        self.assertEqual(purchase.date, self.date)

    def test_purchase_with_multiple_persons(self):
        purchase = Purchase('group_purchase', [self.person1, self.person2], [self.coffee1], self.date)
        self.assertEqual(len(purchase.persons), 2)
        self.assertIn(self.person1, purchase.persons)
        self.assertIn(self.person2, purchase.persons)

    def test_purchase_with_multiple_coffees(self):
        purchase = Purchase('multi_coffee', [self.person1], [self.coffee1, self.coffee2], self.date)
        self.assertEqual(len(purchase.coffees), 2)
        self.assertIn(self.coffee1, purchase.coffees)
        self.assertIn(self.coffee2, purchase.coffees)

    def test_cost_by_one_person_single_coffee(self):
        purchase = Purchase('single', [self.person1, self.person2], [self.coffee1], self.date)
        self.assertEqual(purchase.cost_by_one_person(self.person1), 12)
        self.assertEqual(purchase.cost_by_one_person(self.person2), 8)

    def test_cost_by_one_person_multiple_coffees(self):
        purchase = Purchase('multiple', [self.person1, self.person2], [self.coffee1, self.coffee2], self.date)
        self.assertEqual(purchase.cost_by_one_person(self.person1), 21)
        self.assertEqual(purchase.cost_by_one_person(self.person2), 14)

    def test_cost_by_one_person_no_days(self):
        person_no_days = Person(Name("Zero", "Days"), 0)
        purchase = Purchase('no_days', [person_no_days], [self.coffee1], self.date)
        with self.assertRaises(ValueError):
            purchase.cost_by_one_person(person_no_days)

    def test_invalid_id_setter(self):
        purchase = Purchase('test', [self.person1], [self.coffee1], self.date)
        with self.assertRaises(ValueError):
            purchase.id = -1
        with self.assertRaises(ValueError):
            purchase.id = "invalid"

    def test_string_representation(self):
        purchase = Purchase('test', [self.person1], [self.coffee1], self.date, 1)
        str_repr = str(purchase)
        self.assertIn('test', str_repr)
        self.assertIn('1', str_repr)

    def test_empty_persons_list(self):
        purchase = Purchase('empty', [], [self.coffee1], self.date)
        self.assertEqual(len(purchase.persons), 0)

    def test_empty_coffees_list(self):
        purchase = Purchase('empty', [self.person1], [], self.date)
        self.assertEqual(len(purchase.coffees), 0)

    def test_date_modification(self):
        purchase = Purchase('date_test', [self.person1], [self.coffee1], self.date)
        new_date = datetime(2024, 1, 1)
        purchase.date = new_date
        self.assertEqual(purchase.date, new_date)


if __name__ == '__main__':
    unittest.main()