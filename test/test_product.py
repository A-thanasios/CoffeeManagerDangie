import unittest
from module.data.product import Product


class TestProduct(unittest.TestCase):
    def test_allows_valid_brand_name(self):
        product = Product("Starbucks", "Main Street", 5)
        product.brand_name = "Dunkin"
        self.assertEqual(product.brand_name, "Dunkin")

    def test_raises_error_for_non_string_brand_name(self):
        product = Product("Starbucks", "Main Street", 5)
        with self.assertRaises(ValueError) as context:
            product.brand_name = 123
        self.assertIn("brand_name must be a string", str(context.exception))

    def test_allows_valid_shop(self):
        product = Product("Starbucks", "Main Street", 5)
        product.shop = "Broadway"
        self.assertEqual(product.shop, "Broadway")

    def test_raises_error_for_non_string_shop(self):
        product = Product("Starbucks", "Main Street", 5)
        with self.assertRaises(ValueError) as context:
            product.shop = 456
        self.assertIn("shop must be a string", str(context.exception))

    def test_allows_positive_cost(self):
        product = Product("Starbucks", "Main Street", 5)
        product.cost = 10.5
        self.assertEqual(product.cost, 10.5)

    def test_raises_error_for_negative_cost(self):
        product = Product("Starbucks", "Main Street", 5)
        with self.assertRaises(ValueError) as context:
            product.cost = -5
        self.assertIn("cost must be a positive number", str(context.exception))

    def test_raises_error_for_non_number_cost(self):
        product = Product("Starbucks", "Main Street", 5)
        with self.assertRaises(ValueError) as context:
            product.cost = "free"
        self.assertIn("cost must be a positive number", str(context.exception))

    def test_allows_valid_img(self):
        product = Product("Starbucks", "Main Street", 5, "image.jpg")
        self.assertEqual(product.img, "image.jpg")
        product.img = "new_image.jpg"
        self.assertEqual(product.img, "new_image.jpg")

    def test_str_representation(self):
        product = Product("Starbucks", "Main Street", 5)
        self.assertEqual(str(product), "Starbucks from Main Street, cost= 5")


if __name__ == "__main__":
    unittest.main()
