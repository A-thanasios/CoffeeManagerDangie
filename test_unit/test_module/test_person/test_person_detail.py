import unittest
from MVP.Module.model.data.person_detail import PersonDetail

class TestPersonDetail(unittest.TestCase):
    def test_valid_initialization(self):
        """Test valid initialization of PersonDetail"""
        person_detail = PersonDetail("John Doe", "john@example.com", 5)
        self.assertEqual(person_detail.name, "John Doe")
        self.assertEqual(person_detail.e_mail, "john@example.com")
        self.assertEqual(person_detail.days_per_week, 5)
        self.assertTrue(person_detail.is_buying)  # default value

    def test_invalid_name(self):
        """Test that empty or invalid name raises ValueError"""
        with self.assertRaises(ValueError):
            PersonDetail("", "john@example.com", 5)
        with self.assertRaises(ValueError):
            PersonDetail(None, "john@example.com", 5)

    def test_invalid_email(self):
        """Test that invalid email raises ValueError"""
        with self.assertRaises(ValueError):
            PersonDetail("John Doe", "invalid-email", 5)
        with self.assertRaises(ValueError):
            PersonDetail("John Doe", "", 5)

    def test_invalid_days_per_week(self):
        """Test that invalid days_per_week raises ValueError"""
        with self.assertRaises(ValueError):
            PersonDetail("John Doe", "john@example.com", -1)
        with self.assertRaises(ValueError):
            PersonDetail("John Doe", "john@example.com", 6)
        with self.assertRaises(ValueError):
            PersonDetail("John Doe", "john@example.com", "5")

    def test_invalid_is_buying(self):
        """Test that invalid is_buying raises ValueError"""
        with self.assertRaises(ValueError):
            PersonDetail("John Doe", "john@example.com", 5, is_buying="yes")

if __name__ == "__main__":
    unittest.main()
