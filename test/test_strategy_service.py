import unittest
from datetime import datetime
from unittest.mock import MagicMock
from module.data.person import Person
from module.data.purchase import Purchase
from module.data.product import Product
from module.data.structs.name import Name
from module.services.strategy_service import StrategyService

class TestStrategyService(unittest.TestCase):
    def setUp(self):
        self.person_service = MagicMock()
        self.purchase_service = MagicMock()
        self.product_repo = MagicMock()
        self.by_person_strategy = MagicMock()
        self.strategy_service = StrategyService(
            self.person_service,
            self.purchase_service,
            self.product_repo,
            self.by_person_strategy
        )

        self.person = Person(Name("John", "Bin"), days_per_week=5)
        self.person.id = 1
        self.person2 = Person(Name("Jane", "Doe"), days_per_week=3)
        self.person2.id = 2
        self.product1 = Product("Product1", "Adresa1", 100)
        self.product2 = Product("Product2", "Adresa2", 200)
        self.product3 = Product("Product1", "Adresa1", 160)

    def test_calculates_person_costs_correctly(self):
        purchase1 = Purchase("Purchase1", persons=[self.person], products=[self.product1], date=datetime.now())
        purchase2 = Purchase("Purchase2", persons=[self.person], products=[self.product2], date=datetime.now())
        self.person_service.get.return_value = self.person
        self.person_service.get_all_purchases.return_value = [purchase1, purchase2]
        self.purchase_service.person_has_purchases.return_value = True
        self.by_person_strategy.calculate.side_effect = [50.0, 100.0]

        result = self.strategy_service.calculate_person_costs(self.person.id)

        self.assertEqual(result, {purchase1: 50.0, purchase2: 100.0})

    def test_raises_error_when_person_not_found(self):
        self.person_service.get.side_effect = ValueError("Person not found")

        with self.assertRaises(ValueError) as context:
            self.strategy_service.calculate_person_costs(999)

        self.assertEqual(str(context.exception), "Person not found")

    def test_raises_error_when_person_has_no_purchases(self):
        self.person_service.get.return_value = self.person
        self.purchase_service.person_has_purchases.return_value = False

        with self.assertRaises(ValueError) as context:
            self.strategy_service.calculate_person_costs(self.person.id)

        self.assertEqual(str(context.exception), "Person has no purchases")

    def test_calculates_purchase_costs_correctly(self):
        purchase = Purchase("PurchaseGroup", persons=[self.person, self.person2], products=[self.product3], date=datetime.now())
        purchase.id = 1
        self.purchase_service.get.return_value = purchase
        self.purchase_service.get_all_persons.return_value = [self.person, self.person2]
        self.by_person_strategy.calculate_all.return_value = {self.person: 100.0, self.person2: 60.0}

        result = self.strategy_service.calculate_purchase_costs(purchase.id)

        self.assertEqual(result, {self.person: 100.0, self.person2: 60.0})

    def test_raises_error_when_purchase_not_found(self):
        self.purchase_service.get.side_effect = ValueError("Purchase not found")

        with self.assertRaises(ValueError) as context:
            self.strategy_service.calculate_purchase_costs(999)

        self.assertEqual(str(context.exception), "Purchase not found")


if __name__ == '__main__':
    unittest.main()