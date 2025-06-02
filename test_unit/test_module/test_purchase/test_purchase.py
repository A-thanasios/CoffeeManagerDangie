import unittest
from datetime import datetime

from MVP.Module.model.product import Product
from MVP.Module.model.person import Person
from MVP.Module.model.purchase import Purchase
from MVP.Module.model.data.person_detail import PersonDetail
from MVP.Module.model.data.purchase_detail import PurchaseDetail
from MVP.Module.model.data.purchase_settlement import PurchaseSettlement


class TestPurchase(unittest.TestCase):
    def setUp(self):
        # Valid test data
        self.person_detail = PersonDetail("Alice", "alice@test.com", 3)
        self.person = Person(self.person_detail)
        self.product = Product("Starbucks", "Main Street", 20)
        self.purchase_detail = PurchaseDetail("Test Purchase", datetime.now())
        self.settlement = PurchaseSettlement(self.person, 20)

        # Create a valid purchase
        self.valid_purchase = Purchase(
            self.purchase_detail,
            [self.person],
            [self.product],
            [self.settlement]
        )

        # Invalid test data for purchase_detail
        self.invalid_purchase_details = [
            None,
            "Not a PurchaseDetail",
            123
        ]

        # Invalid test data for persons
        self.invalid_persons_data = [
            None,
            [],  # empty list
            [None],
            ["Not a Person"],
            [123]
        ]

        # Invalid test data for products
        self.invalid_products_data = [
            None,
            ["Not a Product"],
            [123]
        ]

        # Invalid test data for settlements
        self.invalid_settlements_data = [
            None,
            ["Not a Settlement"],
            [123]
        ]

    def test_valid_initialization(self):
        """Test initialization with valid data"""
        self.assertEqual(self.valid_purchase.purchase_detail, self.purchase_detail)
        self.assertEqual(self.valid_purchase.persons, [self.person])
        self.assertEqual(self.valid_purchase.products, [self.product])
        self.assertEqual(self.valid_purchase.purchase_settlements, [self.settlement])
        self.assertIsNone(self.valid_purchase.id)

    def test_invalid_purchase_detail(self):
        """Test initialization with invalid purchase_detail"""
        for invalid_detail in self.invalid_purchase_details:
            with self.assertRaises(ValueError):
                Purchase(invalid_detail, [self.person], [self.product], [self.settlement])

    def test_invalid_persons(self):
        """Test initialization with invalid persons"""
        for invalid_persons in self.invalid_persons_data:
            with self.assertRaises(ValueError):
                Purchase(self.purchase_detail, invalid_persons, [self.product], [self.settlement])

    def test_invalid_products(self):
        """Test initialization with invalid products"""
        for invalid_products in self.invalid_products_data:
            with self.assertRaises(ValueError):
                Purchase(self.purchase_detail, [self.person], invalid_products, [self.settlement])

    def test_invalid_settlements(self):
        """Test initialization with invalid settlements"""
        for invalid_settlements in self.invalid_settlements_data:
            with self.assertRaises(ValueError):
                Purchase(self.purchase_detail, [self.person], [self.product], invalid_settlements)

    def test_invalid_person_settlement_relationship(self):
        """Test invalid relationship between persons and settlements"""
        with self.assertRaises(ValueError):
            Purchase(self.purchase_detail, [self.person], [self.product], [PurchaseSettlement(Person(PersonDetail("Not", "ye@a.tzz", 0)), 20)])
        with self.assertRaises(ValueError):
                    Purchase(self.purchase_detail, [self.person, Person(PersonDetail("Bond", "Dezon@sad.cz", 5))],
                             [self.product], [PurchaseSettlement(Person(PersonDetail("Not", "ye@a.tzz", 0)), 20)])

    def test_empty_persons_products_settlements(self):
        """Test initialization with empty persons, products, or settlements"""
        with self.assertRaises(ValueError):
            Purchase(self.purchase_detail, [], [self.product], [self.settlement])
        with self.assertRaises(ValueError):
            Purchase(self.purchase_detail, [self.person], [], [self.settlement])
        with self.assertRaises(ValueError):
            Purchase(self.purchase_detail, [self.person], [self.product], [])

    def test_id_operations(self):
        """Test ID operations"""
        # Test setting ID for the first time
        purchase = Purchase(self.purchase_detail, [self.person], [self.product], [self.settlement])
        purchase.id = 1
        self.assertEqual(purchase.id, 1)

        # Test that ID cannot be changed once set
        with self.assertRaises(ValueError):
            purchase.id = 2

        # Test invalid ID values
        purchase = Purchase(self.purchase_detail, [self.person], [self.product], [self.settlement])
        with self.assertRaises(ValueError):
            purchase.id = -1
        with self.assertRaises(ValueError):
            purchase.id = "1"


if __name__ == '__main__':
    unittest.main()

