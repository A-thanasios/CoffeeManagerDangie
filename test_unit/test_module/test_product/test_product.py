import unittest
from MVP.Module.model.product import Product


class TestProduct(unittest.TestCase):
    def setUp(self):
        # Valid test data
        self.valid_product = Product("Starbucks", "Main Street", 5)
        self.valid_product_with_id = Product("Costa", "Side Street", 5, db_id=1)

        # Invalid test data
        self.invalid_product_data = [
            ("", "Main Street", 5),  # empty brand_name
            ("Starbucks", "", 5),    # empty shop
            ("Starbucks", "Main Street", -5),  # negative cost
            ("Starbucks", "Main Street", 0),   # zero cost
            ("Starbucks", "Main Street", "5")  # wrong type for cost
        ]

    def test_valid_initialization(self):
        """Test initialization with valid data"""
        self.assertEqual(self.valid_product.brand_name, "Starbucks")
        self.assertEqual(self.valid_product.shop, "Main Street")
        self.assertEqual(self.valid_product.cost, 5)
        self.assertIsNone(self.valid_product.id)

        self.assertEqual(self.valid_product_with_id.id, 1)

    def test_invalid_initialization(self):
        """Test initialization with invalid data"""
        for brand_name, shop, cost in self.invalid_product_data:
            with self.assertRaises(ValueError):
                Product(brand_name, shop, cost)

    def test_id_operations(self):
        """Test ID operations"""
        # Test setting ID for the first time
        product = Product("Starbucks", "Main Street", 5)
        product.id = 1
        self.assertEqual(product.id, 1)

        # Test that ID cannot be changed once set
        with self.assertRaises(ValueError):
            product.id = 2

        # Test invalid ID values
        product = Product("Starbucks", "Main Street", 5)
        with self.assertRaises(ValueError):
            product.id = -1
        with self.assertRaises(ValueError):
            product.id = 0
        with self.assertRaises(ValueError):
            product.id = "1"

    def test_str_representation(self):
        """Test string representation"""
        self.assertEqual(
            str(self.valid_product),
            "Starbucks from Main Street, cost= 5"
        )


if __name__ == "__main__":
    unittest.main()
