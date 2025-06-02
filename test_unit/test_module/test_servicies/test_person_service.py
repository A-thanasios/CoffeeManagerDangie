import unittest
from datetime import datetime
from unittest.mock import MagicMock
from MVP.Module.model.person import Person
from MVP.Module import Purchase
from MVP.Module import PersonDetail
from MVP.Module import PersonService

class TestPersonService(unittest.TestCase):
    def setUp(self):
        self.repo = MagicMock()
        self.purchase_service = MagicMock()
        self.person_service = PersonService(self.repo, self.purchase_service)

        self.person = Person(PersonDetail("John", "Bin"), 5)
        self.person.id = 1
        self.person2 = Person(PersonDetail("Jane", "Doe"), 3)
        self.person2.id = 2

    def test_add_person_success(self):
        self.repo.get_all.return_value = []
        self.repo.add.return_value = self.person.id
        result = self.person_service.create(self.person)
        self.assertEqual(result, self.person.id)
        self.repo.add.assert_called_once_with(self.person)

    def test_add_person_already_exists(self):
        self.repo.get_all.return_value = [self.person]
        with self.assertRaises(ValueError) as context:
            self.person_service.create(self.person)
        self.assertEqual(str(context.exception), "Person already exists")

    def test_add_person_invalid_arg(self):
        with self.assertRaises(ValueError) as context:
            self.person_service.create("not a person")
        self.assertEqual(str(context.exception), "arg must be a Person object")

    def test_get_person_success(self):
        self.repo.get_by_id.return_value = self.person
        result = self.person_service.get(self.person.id)
        self.assertEqual(result, self.person)
        self.repo.get_by_id.assert_called_once_with(self.person.id)

    def test_get_person_not_found(self):
        self.repo.get_by_id.return_value = None
        with self.assertRaises(ValueError) as context:
            self.person_service.get(999)
        self.assertEqual(str(context.exception), "Purchase not found")

    def test_get_person_invalid_id(self):
        with self.assertRaises(ValueError) as context:
            self.person_service.get(-1)
        self.assertEqual(str(context.exception), "ID must be a positive integer")

    def test_get_all_success(self):
        self.repo.get_all.return_value = [self.person, self.person2]
        result = self.person_service.get_all()
        self.assertEqual(result, [self.person, self.person2])
        self.repo.get_all.assert_called_once()

    def test_get_all_empty(self):
        self.repo.get_all.return_value = []
        with self.assertRaises(ValueError) as context:
            self.person_service.get_all()
        self.assertEqual(str(context.exception), "No persons found")

    def test_get_all_purchases_success(self):
        self.purchase_service.get_all_persons.return_value = [self.person]
        mock_purchase = Purchase("TestPurchase", [self.person], [], datetime.now())
        self.purchase_service.get.return_value = mock_purchase

        result = self.person_service.get_all_purchases(self.person.id)
        self.assertEqual(result, [mock_purchase])
        self.purchase_service.get_all_persons.assert_called_once_with(self.person.id)
        self.purchase_service.get.assert_called_once_with(self.person)

    def test_get_all_purchases_no_persons(self):
        self.purchase_service.get_all_persons.return_value = []
        with self.assertRaises(ValueError) as context:
            self.person_service.get_all_purchases(self.person.id)
        self.assertEqual(str(context.exception), "No persons found")


    def test_remove_person_success(self):
        self.repo.get_by_id.return_value = self.person
        self.purchase_service.person_has_purchases.return_value = False

        self.person_service.remove(self.person.id)
        self.repo.remove_by_id.assert_called_once_with(self.person.id)

    def test_remove_person_not_found(self):
        self.repo.get_by_id.return_value = None
        with self.assertRaises(ValueError) as context:
            self.person_service.remove(999)
        self.assertEqual(str(context.exception), "Person not found")

    def test_remove_person_has_purchases(self):
        self.repo.get_by_id.return_value = self.person
        self.purchase_service.person_has_purchases.return_value = True
        with self.assertRaises(ValueError) as context:
            self.person_service.remove(self.person.id)
        self.assertEqual(str(context.exception), "Person has purchases, cannot delete")

    def test_update_person_success(self):
        self.repo.get_by_id.return_value = self.person
        self.person_service.update(self.person)
        self.repo.update.assert_called_once_with(self.person)

    def test_update_person_not_found(self):
        self.repo.get_by_id.return_value = None
        with self.assertRaises(ValueError) as context:
            self.person_service.update(self.person)
        self.assertEqual(str(context.exception), "Person not found")

    def test_update_person_invalid_arg(self):
        with self.assertRaises(ValueError) as context:
            self.person_service.update("not a person")
        self.assertEqual(str(context.exception), "arg must be a Person object")

if __name__ == '__main__':
    unittest.main()