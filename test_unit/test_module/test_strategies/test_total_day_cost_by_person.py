import unittest
from MVP_DEPRECATED.Module.Model.person import Person
from MVP_DEPRECATED.Module.Model.product import Product
from MVP_DEPRECATED.Module import Purchase
from MVP_DEPRECATED.Module import PersonDetail
from MVP_DEPRECATED.Module.strategies.by_person_strategy import ByPersonStrategy
from datetime import datetime


class TestTotalDayCostByPerson(unittest.TestCase):
    def setUp(self):
        self.person1 = Person(PersonDetail("Alice", "Wonderland"), 3)
        self.person2 = Person(PersonDetail("Bob", "Builder"), 2)
        self.product1 = Product("Starbucks", "Main Street", 20)
        self.product2 = Product("Costa", "Side Street", 15)
        self.purchase = Purchase(
            "Test Purchase", [self.person1, self.person2], [self.product1, self.product2], datetime.now()
        )
        self.strategy = ByPersonStrategy()

    def test_calculate_cost_for_person(self):
        cost = self.strategy.calculate(self.purchase, self.person1)
        self.assertAlmostEqual(cost, 21.0, places=2)

    def test_calculate_cost_with_no_days(self):
        person_no_days = Person(PersonDetail("Zero", "Days"), 0)
        with self.assertRaises(ValueError):
            self.strategy.calculate(self.purchase, person_no_days)

    def test_calculate_cost_with_single_product(self):
        purchase = Purchase("Single Product", [self.person1, self.person2], [self.product1], datetime.now())
        cost = self.strategy.calculate(purchase, self.person2)
        self.assertAlmostEqual(cost, 8.0, places=2)


if __name__ == "__main__":
    unittest.main()
