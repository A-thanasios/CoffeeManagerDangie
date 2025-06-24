import unittest
from MVP_DEPRECATED.Module.Model.person import Person
from MVP_DEPRECATED.Module.Model.data.person_detail import PersonDetail

class TestPerson(unittest.TestCase):
    def setUp(self):
        """Set up test cases"""
        self.test_person_detail = PersonDetail(
            name="John Doe",
            e_mail="john@example.com",
            days_per_week=5
        )
        self.test_person = Person(self.test_person_detail)

    def test_initialization(self):
        """Test proper initialization"""
        self.assertEqual(self.test_person.person_detail_dict, self.test_person_detail)
        self.assertIsNone(self.test_person.id)

    def test_initialization_with_id(self):
        """Test initialization with ID"""
        person = Person(self.test_person_detail, db_id=1)
        self.assertEqual(person.id, 1)

    def test_id_setter(self):
        """Test ID setter"""
        self.test_person.id = 1
        self.assertEqual(self.test_person.id, 1)

        # Test that ID cannot be changed once set
        with self.assertRaises(ValueError):
            self.test_person.id = 2

        # Test invalid ID values
        person = Person(self.test_person_detail)
        with self.assertRaises(ValueError):
            person.id = -1
        with self.assertRaises(ValueError):
            person.id = "1"

    def test_person_detail_property(self):
        """Test person_detail property"""
        self.assertEqual(self.test_person.person_detail_dict, self.test_person_detail)

if __name__ == '__main__':
    unittest.main()

