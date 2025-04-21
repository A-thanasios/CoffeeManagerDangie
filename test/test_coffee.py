import unittest
from module.data.coffee import Coffee


class TestCoffee(unittest.TestCase):
    def test_allows_valid_brand_name(self):
        coffee = Coffee("Starbucks", "Main Street", 5)
        coffee.brand_name = "Dunkin"
        self.assertEqual(coffee.brand_name, "Dunkin")

    def test_raises_error_for_non_string_brand_name(self):
        coffee = Coffee("Starbucks", "Main Street", 5)
        with self.assertRaises(ValueError) as context:
            coffee.brand_name = 123
        self.assertIn("brand_name must be a string", str(context.exception))

    def test_allows_valid_shop(self):
        coffee = Coffee("Starbucks", "Main Street", 5)
        coffee.shop = "Broadway"
        self.assertEqual(coffee.shop, "Broadway")

    def test_raises_error_for_non_string_shop(self):
        coffee = Coffee("Starbucks", "Main Street", 5)
        with self.assertRaises(ValueError) as context:
            coffee.shop = 456
        self.assertIn("shop must be a string", str(context.exception))

    def test_allows_positive_cost(self):
        coffee = Coffee("Starbucks", "Main Street", 5)
        coffee.cost = 10.5
        self.assertEqual(coffee.cost, 10.5)

    def test_raises_error_for_negative_cost(self):
        coffee = Coffee("Starbucks", "Main Street", 5)
        with self.assertRaises(ValueError) as context:
            coffee.cost = -5
        self.assertIn("cost must be a positive number", str(context.exception))

    def test_raises_error_for_non_number_cost(self):
        coffee = Coffee("Starbucks", "Main Street", 5)
        with self.assertRaises(ValueError) as context:
            coffee.cost = "free"
        self.assertIn("cost must be a positive number", str(context.exception))


if __name__ == "__main__":
    unittest.main()