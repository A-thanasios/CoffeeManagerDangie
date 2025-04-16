import unittest
from datetime import datetime

from src.coffee_payment_calculator import CoffeePaymentCalculator
from src.data.coffee import Coffee
from src.data.person import Person
from src.data.purchase import Purchase
from src.data.structs.name import Name

class TestCoffeePaymentCalculator(unittest.TestCase):
    def setUp(self):
        self.coffee = Coffee("Starbucks", "Main Street", 20)
        self.person = Person(Name("Alice", "Wonderland"), 3)
        self.person2 = Person(Name("Bob", "La Blob"), 2)
        self.date = datetime.now()

    def test_calculates_cost_correctly_for_multiple_persons(self):

        purchase = Purchase('purchase',[self.person, self.person2], self.coffee, self.date)
        calculator = CoffeePaymentCalculator()
        result = calculator.cost_by_one_person(purchase, self.coffee, self.person)
        self.assertEqual(result, 12)  # (20 * 3) / (3 + 2)

    def test_raises_error_when_no_persons_in_purchase(self):
        purchase = Purchase('purchase',[], self.coffee, self.date)
        calculator = CoffeePaymentCalculator()

        with self.assertRaises(ValueError) as context:
            calculator.cost_by_one_person(purchase, self.coffee, self.person)
        self.assertIn("No days sum available", str(context.exception))

    def test_calculates_cost_correctly_when_one_person_has_zero_days(self):
        person1 = self.person
        person1.days_per_week = 0
        purchase = Purchase('purchase',[person1, self.person2], self.coffee, self.date)
        calculator = CoffeePaymentCalculator()

        result = calculator.cost_by_one_person(purchase, self.coffee, self.person2)
        self.assertEqual(result, 20)  # (20 * 5) / (0 + 5)

    def test_handles_zero_cost_coffee(self):
        coffee = self.coffee
        coffee.cost = 0
        purchase = Purchase('purchase',[self.person], coffee, self.date)
        calculator = CoffeePaymentCalculator()

        result = calculator.cost_by_one_person(purchase, coffee, self.person)
        self.assertEqual(result, 0)

if __name__ == "__main__":
    unittest.main()