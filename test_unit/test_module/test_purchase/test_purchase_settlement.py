import unittest
from MVP.Module.model.person import Person
from MVP.Module.model.data.person_detail import PersonDetail
from MVP.Module.model.data.purchase_settlement import PurchaseSettlement


class TestPurchaseSettlement(unittest.TestCase):
    def setUp(self):
        # Valid test data
        self.person_detail = PersonDetail("John", "john@test.com", 5)
        self.person = Person(self.person_detail)
        self.amount = 100.0
        self.valid_settlement = PurchaseSettlement(self.person, self.amount)

        # Invalid test data
        self.invalid_persons = [
            None,
            "Not a Person",
            123,
            []
        ]

        self.invalid_amounts = [
            None,
            "100",  # string
            [],  # list
        ]

    def test_valid_initialization(self):
        """Test initialization with valid data"""
        settlement = PurchaseSettlement(self.person, self.amount)
        self.assertEqual(settlement.person, self.person)
        self.assertEqual(settlement.amount, self.amount)
        self.assertFalse(settlement.is_paid)

    def test_invalid_person(self):
        """Test initialization with invalid person"""
        for invalid_person in self.invalid_persons:
            with self.assertRaises(ValueError):
                PurchaseSettlement(invalid_person, self.amount)

    def test_invalid_amount(self):
        """Test initialization with invalid amount"""
        for invalid_amount in self.invalid_amounts:
            with self.assertRaises(ValueError):
                PurchaseSettlement(self.person, invalid_amount)

    def test_custom_is_paid(self):
        """Test setting custom is_paid value"""
        settlement = PurchaseSettlement(self.person, self.amount, True)
        self.assertTrue(settlement.is_paid)


if __name__ == '__main__':
    unittest.main()
