import gc
import os
import unittest
import time
from datetime import datetime

from Infrastructure import DatabaseFactory, RepositoryFactory
from Module import PersonService, ProductService, PurchaseService, StrategyExecutor
from Module.Model.person import Person
from Module.Model.purchase import Purchase


class PurchaseTest(unittest.TestCase):
    def setUp(self):
        # Initialize the database
        self.db = DatabaseFactory.create_test_database()

        # Initialize the repositories
        person_repository = RepositoryFactory(self.db).create_person_repository()
        product_repository = RepositoryFactory(self.db).create_product_repository()
        purchase_repository = RepositoryFactory(self.db).create_purchase_repository()

        # Initialize the services
        self.person_service = PersonService(person_repository)
        product_service = ProductService(product_repository)
        self.strategy_service = StrategyExecutor()
        self.purchase_service = PurchaseService(purchase_repository,
                                            product_service,
                                           self.person_service,
                                           self.strategy_service
                                            )

    def tearDown(self):
        gc.collect()
        time.sleep(0.1)
        os.remove(self.db.path)


    def test_person_create(self):
        person_id = self.person_service.create(name="John Doe",
                                            e_mail="boi@umcala.com",
                                            days_per_week=5,
                                            is_buying=True)

        person_from_db = Person(**self.person_service.read(person_id))
        self.assertIsNotNone(person_from_db)
        self.assertEqual(person_from_db.detail.name, "John Doe")

    def test_person_delete(self):
        person_id = self.person_service.create(name="John Doe",
                                               e_mail="boi@umcala.com",
                                               days_per_week=5,
                                               is_buying=True)

        self.person_service.remove(person_id)

        self.assertRaises(
            ValueError,
            self.person_service.read,
            person_id
        )

    def test_person_update(self):
        person_id = self.person_service.create(name="John Doe",
                                               e_mail="boi@umcala.com",
                                               days_per_week=5,
                                               is_buying=True)

        self.person_service.update(person_id, days_per_week=3, is_buying=False)

        updated_person = Person(**self.person_service.read(person_id))
        self.assertEqual(updated_person.detail.days_per_week, 3)
        self.assertFalse(updated_person.detail.is_buying)

    def test_purchase_create(self):
        john_id = self.person_service.create(   name="John Doe",
                                                e_mail="boi@umcala.com",
                                                days_per_week=5,
                                                is_buying=True)

        erika_id = self.person_service.create(  name="Erika",
                                                e_mail="erika@umcala.com",
                                                days_per_week=2)

        products = [
            ("Star", "Sky", 500)
        ]

        purchase_id = self.purchase_service.create(name="Test Purchase", date=datetime.now(),
                                                    person_ids=[john_id, erika_id],
                                                    products=products,
                                                    strategy_type="ByPerson"
                                                   )
        purchase_serial = self.purchase_service.read(purchase_id)
        purchase = Purchase(name=purchase_serial['name'], date=purchase_serial['date'],
                            purchase_settlements=[tuple([settlement['person'],
                                                         settlement['amount'],
                                                         settlement['is_paid']])
                                                  for settlement in purchase_serial['purchase_settlements']],
                            products=purchase_serial['products']
                            )
        self.assertIsNotNone(purchase)
        self.assertEqual(purchase.detail.name, "Test Purchase")
        self.assertEqual(len(purchase.persons), 2)
        self.assertEqual(len(purchase.products), 1)
        self.assertEqual(len(purchase.purchase_settlements_dict), 2)
        for settlement in purchase.purchase_settlements:
            if settlement.person.id == john_id:
                self.assertEqual(round(settlement.amount), 357)
            if settlement.person.id == erika_id:
                self.assertEqual(round(settlement.amount), 143)

    def test_purchase_delete(self):
        john_id = self.person_service.create(name="John Doe",
                                             e_mail="boi@umcala.com",
                                             days_per_week=5,
                                             is_buying=True)

        erika_id = self.person_service.create(name="Erika",
                                              e_mail="erika@umcala.com",
                                              days_per_week=2)

        products = [
            ("Star", "Sky", 500)
        ]

        purchase_id = self.purchase_service.create(name="Test Purchase", date=datetime.now(),
                                                   person_ids=[john_id, erika_id],
                                                   products=products,
                                                   strategy_type="ByPerson"
                                                   )
        purchase_serial = self.purchase_service.read(purchase_id)
        purchase = Purchase(name=purchase_serial['name'], date=purchase_serial['date'],
                            purchase_settlements=[tuple([settlement['person'],
                                                         settlement['amount'],
                                                         settlement['is_paid']])
                                                  for settlement in purchase_serial['purchase_settlements']],
                            products=purchase_serial['products']
                            )
        self.assertEqual(purchase.detail.name, "Test Purchase")
        self.purchase_service.remove(purchase_id)
        self.assertRaises(
            ValueError,
            self.purchase_service.read,
            purchase_id
        )
        purchase_id = self.purchase_service.create(name="Test Purchase", date=datetime.now(),
                                                   person_ids=[john_id, erika_id],
                                                   products=products,
                                                   strategy_type="ByPerson"
                                                   )
        purchase_serial = self.purchase_service.read(purchase_id)
        purchase = Purchase(name=purchase_serial['name'], date=purchase_serial['date'],
                            purchase_settlements=[tuple([settlement['person'],
                                                         settlement['amount'],
                                                         settlement['is_paid']])
                                                  for settlement in purchase_serial['purchase_settlements']],
                            products=purchase_serial['products']
                            )
        self.assertEqual(purchase.detail.name, "Test Purchase")
