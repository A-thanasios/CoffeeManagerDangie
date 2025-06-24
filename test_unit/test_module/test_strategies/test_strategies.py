import unittest
from datetime import datetime
from MVP_DEPRECATED.Module.Model.product import Product
from MVP_DEPRECATED.Module.Model.person import Person
from MVP_DEPRECATED.Module import Purchase
from MVP_DEPRECATED.Module import PersonDetail
from MVP_DEPRECATED.Module.strategies.by_person_strategy import ByPersonStrategy


class TestTotalDayCostByPerson(unittest.TestCase):
    def setUp(self):
        self.strategy = ByPersonStrategy()

        self.product1 = Product("Starbucks", "Main Street", 20)
        self.product2 = Product("Costa", "Side Street", 15)

        self.person1 = Person(PersonDetail("Alice", "Wonderland"), 3)
        self.person2 = Person(PersonDetail("Bob", "La Blob"), 2)

        self.date = datetime.now()

    def test_calculate_single_person_single_product(self):
        purchase = Purchase("single", [self.person1], [self.product1], self.date)
        cost = self.strategy.calculate(purchase, self.person1)
        self.assertEqual(cost, 20)

    def test_calculate_multiple_persons_single_product(self):
        purchase = Purchase("group", [self.person1, self.person2], [self.product1], self.date)
        cost_person1 = self.strategy.calculate(purchase, self.person1)
        cost_person2 = self.strategy.calculate(purchase, self.person2)
        self.assertAlmostEqual(cost_person1, 12)
        self.assertAlmostEqual(cost_person2, 8)

    def test_calculate_multiple_persons_multiple_products(self):
        purchase = Purchase("multi", [self.person1, self.person2], [self.product1, self.product2], self.date)
        cost_person1 = self.strategy.calculate(purchase, self.person1)
        cost_person2 = self.strategy.calculate(purchase, self.person2)
        self.assertAlmostEqual(cost_person1, 21)
        self.assertAlmostEqual(cost_person2, 14)

    def test_calculate_all(self):
        purchase = Purchase("all", [self.person1, self.person2], [self.product1], self.date)
        costs = self.strategy.calculate_all(purchase)
        self.assertAlmostEqual(costs[self.person1], 12)
        self.assertAlmostEqual(costs[self.person2], 8)

    def test_calculate_no_days_sum(self):
        person_no_days = Person(PersonDetail("Zero", "Days"), 0)
        purchase = Purchase("no_days", [person_no_days], [self.product1], self.date)
        with self.assertRaises(ValueError):
            self.strategy.calculate(purchase, person_no_days)


if __name__ == "__main__":
    unittest.main()