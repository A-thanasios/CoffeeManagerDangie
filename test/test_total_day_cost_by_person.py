import unittest
from module.data.person import Person
from module.data.product import Product
from module.data.purchase import Purchase
from module.data.structs.name import Name
from module.strategies.by_person_strategy import ByPersonStrategy
from datetime import datetime


class TestTotalDayCostByPerson(unittest.TestCase):
    def setUp(self):
        self.person1 = Person(Name("Alice", "Wonderland"), 3)
        self.person2 = Person(Name("Bob", "Builder"), 2)
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
        person_no_days = Person(Name("Zero", "Days"), 0)
        with self.assertRaises(ValueError):
            self.strategy.calculate(self.purchase, person_no_days)

    def test_calculate_cost_with_single_product(self):
        purchase = Purchase("Single Product", [self.person1, self.person2], [self.product1], datetime.now())
        cost = self.strategy.calculate(purchase, self.person2)
        self.assertAlmostEqual(cost, 8.0, places=2)


if __name__ == "__main__":
    unittest.main()
