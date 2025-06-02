# test_unit/test_purchase_service.py
import unittest
from datetime import datetime
from unittest.mock import MagicMock
from MVP.Module.model.person import Person
from MVP.Module import Purchase
from MVP.Module.model.product import Product
from MVP.Module import PersonDetail
from MVP.Module.services.purchase_service import PurchaseService

class TestPurchaseService(unittest.TestCase):
    def setUp(self):
        self.repo = MagicMock()
        self.purchase_service = PurchaseService(self.repo)

        self.person = Person(PersonDetail("John", "Bin"), 5)
        self.person.id = 1
        self.product = Product("Product1", "Adresa1", 100)
        self.purchase = Purchase("Purchase1", persons=[self.person], products=[self.product], date=datetime.now())
        self.purchase.id = 1

    def test_add_purchase_success(self):
        self.repo.get_all.return_value = []
        self.repo.add.return_value = self.purchase.id
        result = self.purchase_service.add(self.purchase)
        self.assertEqual(result, self.purchase.id)
        self.repo.add.assert_called_once_with(self.purchase)

    def test_add_purchase_already_exists(self):
        self.repo.get_all.return_value = [self.purchase]
        with self.assertRaises(ValueError) as context:
            self.purchase_service.add(self.purchase)
        self.assertEqual(str(context.exception), "Purchase already exists")

    def test_add_purchase_invalid_arg(self):
        with self.assertRaises(ValueError) as context:
            self.purchase_service.add("not a purchase")
        self.assertEqual(str(context.exception), "arg must be a Purchase object")

    def test_get_purchase_success(self):
        self.repo.get_by_id.return_value = self.purchase
        result = self.purchase_service.get(self.purchase.id)
        self.assertEqual(result, self.purchase)
        self.repo.get_by_id.assert_called_once_with(self.purchase.id)

    def test_get_purchase_not_found(self):
        self.repo.get_by_id.return_value = None
        with self.assertRaises(ValueError) as context:
            self.purchase_service.get(999)
        self.assertEqual(str(context.exception), "Purchase not found")

    def test_get_purchase_invalid_id(self):
        with self.assertRaises(ValueError) as context:
            self.purchase_service.get(-1)
        self.assertEqual(str(context.exception), "ID must be a positive integer")

    def test_get_all_success(self):
        self.repo.get_all.return_value = [self.purchase]
        result = self.purchase_service.get_all()
        self.assertEqual(result, [self.purchase])
        self.repo.get_all.assert_called_once()

    def test_get_all_empty(self):
        self.repo.get_all.return_value = []
        with self.assertRaises(ValueError) as context:
            self.purchase_service.get_all()
        self.assertEqual(str(context.exception), "No purchases found")

    def test_remove_purchase_success(self):
        self.repo.get_by_id.return_value = self.purchase
        self.purchase_service.remove(self.purchase.id)
        self.repo.remove_by_id.assert_called_once_with(self.purchase.id)

    def test_remove_purchase_not_found(self):
        self.repo.get_by_id.return_value = None
        with self.assertRaises(ValueError) as context:
            self.purchase_service.remove(999)
        self.assertEqual(str(context.exception), "Purchase not found")

    def test_update_purchase_success(self):
        self.repo.get_by_id.return_value = self.purchase
        self.purchase_service.update(self.purchase)
        self.repo.update.assert_called_once_with(self.purchase)

    def test_update_purchase_not_found(self):
        self.repo.get_by_id.return_value = None
        with self.assertRaises(ValueError) as context:
            self.purchase_service.update(self.purchase)
        self.assertEqual(str(context.exception), "Purchase not found")

    def test_update_purchase_invalid_arg(self):
        with self.assertRaises(ValueError) as context:
            self.purchase_service.update("not a purchase")
        self.assertEqual(str(context.exception), "arg must be a Purchase object")

    def test_person_has_purchases_true(self):
        self.repo.get_by_other_id.return_value = self.purchase
        result = self.purchase_service.person_has_purchases(self.person.id)
        self.assertTrue(result)
        self.repo.get_by_other_id.assert_called_once_with(self.person.id)

    def test_person_has_purchases_false(self):
        self.repo.get_by_other_id.return_value = None
        result = self.purchase_service.person_has_purchases(self.person.id)
        self.assertFalse(result)

    def test_get_all_persons_success(self):
        self.repo.get_by_id.return_value = self.purchase
        result = self.purchase_service.get_all_persons(self.purchase.id)
        self.assertEqual(result, self.purchase.persons)
        self.repo.get_by_id.assert_called_once_with(self.purchase.id)

    def test_get_all_persons_purchase_not_found(self):
        self.repo.get_by_id.return_value = None
        with self.assertRaises(ValueError) as context:
            self.purchase_service.get_all_persons(999)
        self.assertEqual(str(context.exception), "Purchase not found")

if __name__ == '__main__':
    unittest.main()