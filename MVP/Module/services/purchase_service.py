from MVP.Module.model.person import Person
from MVP.Module import Purchase
from MVP.Module.interfaces.crud_service import CRUDService
from MVP.Module.interfaces.repository import Repository


class PurchaseService(CRUDService):
    def __init__(self, repo: Repository) -> None:
        self.repo = repo

    def add(self, purchase: Purchase) -> Purchase.id:
        print('aaaa')
        if not isinstance(purchase, Purchase):
            raise ValueError("arg must be a Purchase object")

        purchases = self.repo.get_all()
        for p in purchases:
            if p == purchase:
                raise ValueError("Purchase already exists")

        return self.repo.create(purchase)

    def get(self, purchase_id: Purchase.id) -> Purchase:
        if not isinstance(purchase_id, int) or purchase_id < 0:
            raise ValueError("ID must be a positive integer")

        purchase = self.repo.get_by_id(purchase_id)
        if not purchase:
            raise ValueError("Purchase not found")

        return purchase

    def get_all(self) -> list[Purchase]:
        lst = self.repo.get_all()

        if not lst:
            return []

        return lst

    def remove(self, purchase_id: Purchase.id) -> None:
        if not isinstance(purchase_id, int) or purchase_id < 0:
            raise ValueError("ID must be a positive integer")
        if not self.repo.get_by_id(purchase_id):
            raise ValueError("Purchase not found")

        self.repo.delete_by_id(purchase_id)

    def update(self, purchase: Purchase) -> None:
        if not isinstance(purchase, Purchase):
            raise ValueError("arg must be a Purchase object")
        if not self.repo.get_by_id(purchase.id):
            raise ValueError("Purchase not found")

        self.repo.update(purchase)

    def person_has_purchases(self, person_id: int) -> bool:
        return self.repo.get_by_other_id(person_id) != []

    def get_all_persons(self, purchase_id: int) -> list[Person]:
        if not isinstance(purchase_id, int) or purchase_id < 0:
            raise ValueError("ID must be a positive integer")

        purchase = self.repo.get_by_id(purchase_id)
        if not purchase:
            raise ValueError("Purchase not found")

        return purchase.persons