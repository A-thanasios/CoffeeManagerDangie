import unittest
from datetime import datetime
from MVP_DEPRECATED.Module.Model.data.purchase_detail import PurchaseDetail


class TestPurchaseDetail(unittest.TestCase):
    def setUp(self):
        # Valid test data
        self.name = "Test Purchase"
        self.date = datetime.now()
        self.valid_purchase_detail = PurchaseDetail(self.name, self.date)

        # Invalid test data
        self.invalid_names = [
            "",  # empty string
            None,  # None
            123,  # number
            []  # list
        ]

        self.invalid_dates = [
            None,
            "2024-01-01",  # string
            123,  # number
            []  # list
        ]

    def test_valid_initialization(self):
        """Test initialization with valid data"""
        purchase_detail = PurchaseDetail(self.name, self.date)
        self.assertEqual(purchase_detail.name, self.name)
        self.assertEqual(purchase_detail.date, self.date)

    def test_invalid_name(self):
        """Test initialization with invalid name"""
        for invalid_name in self.invalid_names:
            with self.assertRaises(ValueError):
                PurchaseDetail(invalid_name, self.date)

    def test_invalid_date(self):
        """Test initialization with invalid date"""
        for invalid_date in self.invalid_dates:
            with self.assertRaises(ValueError):
                PurchaseDetail(self.name, invalid_date)


if __name__ == '__main__':
    unittest.main()
