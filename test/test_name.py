import unittest
from src.data.structs.name import Name


class TestName(unittest.TestCase):
    def test_allows_valid_first_name(self):
        name = Name("John", "Doe")
        self.assertEqual(name.first_name, "John")

    def test_allows_valid_last_name(self):
        name = Name("John", "Doe")
        self.assertEqual(name.last_name, "Doe")

    def test_allows_valid_middle_name(self):
        name = Name("John", "Doe", "Michael")
        self.assertEqual(name.middle_name, "Michael")

    def test_handles_missing_middle_name(self):
        name = Name("John", "Doe")
        self.assertIsNone(name.middle_name)

    def test_returns_correct_full_name_with_middle_name(self):
        name = Name("John", "Doe", "Michael")
        self.assertEqual(name.full_name, "John Michael Doe")

    def test_returns_correct_full_name_without_middle_name(self):
        name = Name("John", "Doe")
        self.assertEqual(name.full_name, "John Doe")

    def test_str_returns_full_name(self):
        name = Name("John", "Doe", "Michael")
        self.assertEqual(str(name), "John Michael Doe")


if __name__ == "__main__":
    unittest.main()