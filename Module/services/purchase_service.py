from datetime import datetime

from Module.Model.person import Person
from Module.Model.product import Product
from Module.Model.purchase import Purchase

from Module.Interfaces import CRUDService
from Module.Interfaces import Repository
from Module.services.strategy_executor import StrategyExecutor
from Module.strategies.strategy_type import StrategyType


class PurchaseService(CRUDService):
    def __init__(self, repo: Repository,
                 product_service: CRUDService, person_service: CRUDService, strategy_service: StrategyExecutor) -> None:
        self.repo = repo
        self.product_service = product_service
        self.person_service = person_service
        self.strategy_service = strategy_service

    def create(self,
               person_ids: list[int],
               products: list[tuple], strategy_type: str, **kwargs) -> int:

            strategy = StrategyType[strategy_type]
            product_list: list[Product] = [self.product_service.create(*product) for product in products]
            persons = [Person(**self.person_service.read(person_id)) for person_id in person_ids]

            if not persons:
                raise ValueError("No persons found")

            purchases = self.repo.read_all()
            for p in purchases:
                if p == (kwargs["name"]):
                    raise ValueError("Purchase already exists")

            person_costs = self.strategy_service.calculate_costs(strategy,
                                                                 products= product_list,
                                                                 persons=persons)
            purchase = Purchase(**kwargs,
                                purchase_settlements=person_costs,
                                products=product_list,
                                )

            return self.repo.create(purchase)

    def read(self, purchase_id: int) -> dict[str: any]:
        if not isinstance(purchase_id, int) or purchase_id < 0:
            raise ValueError("ID must be a positive integer")

        purchase: Purchase = self.repo.read_by_id(purchase_id)
        if not purchase:
            raise ValueError("Purchase not found")

        return self.__purchase_serialization(purchase)



    def read_all(self) -> list[dict]:
        purchases = self.repo.read_all()
        if not purchases:
            return []

        lst = []

        for purchase in purchases:
            lst.append(self.__purchase_serialization(purchase))

        return lst

    def remove(self, purchase_id: Purchase.id) -> None:
        if not isinstance(purchase_id, int) or purchase_id < 0:
            raise ValueError("ID must be a positive integer")
        if not self.repo.read_by_id(purchase_id):
            raise ValueError("Purchase not found")

        self.repo.delete_by_id(purchase_id)

    def update(self, purchase: Purchase) -> bool:
        if not isinstance(purchase, Purchase):
            raise ValueError("arg must be a Purchase object")
        if not self.repo.read_by_id(purchase.id):
            raise ValueError("Purchase not found")

        self.repo.update(purchase)

    def person_has_purchases(self, person_id: int) -> bool:
        return self.repo.read_by_other_id(person_id) != []

    def get_all_persons(self, purchase_id: int) -> list[Person]:
        if not isinstance(purchase_id, int) or purchase_id < 0:
            raise ValueError("ID must be a positive integer")

        purchase: Purchase = self.repo.read_by_id(purchase_id)
        if not purchase:
            raise ValueError("Purchase not found")

        return purchase.persons

    @staticmethod
    def __purchase_serialization(purchase: Purchase) -> dict:
        detail = purchase.purchase_detail_dict
        settlements = purchase.purchase_settlements_dict

        return {
            **detail,
            "db_id": purchase.id,
            "purchase_settlements": settlements,
            "products": purchase.products
        }