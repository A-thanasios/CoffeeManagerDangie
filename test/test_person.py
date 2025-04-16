import unittest

from src.data.person import Person
from src.data.structs.name import Name


class TestPerson(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.test_name = Name("John", "Doe")
        self.test_person = Person(self.test_name, 5, "test.jpg")
    
    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.test_person.name, self.test_name)
        self.assertEqual(self.test_person.days_per_week, 5)
        self.assertEqual(self.test_person.img, "test.jpg")
    
    def test_name_property(self):
        """Test name property and setter"""
        # Test getter
        self.assertEqual(self.test_person.name, self.test_name)
        
        # Test setter with valid Name object
        new_name = Name("Jane", "Smith")
        self.test_person.name = new_name
        self.assertEqual(self.test_person.name, new_name)
        
        # Test setter with invalid type
        with self.assertRaises(ValueError):
            self.test_person.name = "Invalid Name"
    
    def test_days_per_week_property(self):
        """Test days_per_week property and setter"""
        # Test getter
        self.assertEqual(self.test_person.days_per_week, 5)
        
        # Test setter with valid values
        self.test_person.days_per_week = 3
        self.assertEqual(self.test_person.days_per_week, 3)
        
        # Test setter with invalid types
        with self.assertRaises(ValueError):
            self.test_person.days_per_week = "5"
        
        # Test setter with negative value
        with self.assertRaises(ValueError):
            self.test_person.days_per_week = -1
        
        # Test setter with value > 5
        with self.assertRaises(ValueError):
            self.test_person.days_per_week = 6
    
    def test_img_property(self):
        """Test img property and setter"""
        # Test getter
        self.assertEqual(self.test_person.img, "test.jpg")
        
        # Test setter with new value
        self.test_person.img = "new.jpg"
        self.assertEqual(self.test_person.img, "new.jpg")
        
        # Test setter with empty string
        self.test_person.img = ""
        self.assertEqual(self.test_person.img, "")


if __name__ == '__main__':
    unittest.main() 