from module.data.purchase import Purchase
from module.interfaces.crud_service import CRUDService
from module.interfaces.repository import Repository


class PurchaseService(CRUDService):
    def __init__(self, repo: Repository) -> None:
        self.repo = repo

    def add(self, purchase: Purchase) -> Purchase.id:
        pass

    def get(self, purchase_id: Purchase.id) -> Purchase:
        pass

    def get_all(self) -> list[Purchase]:
        pass

    def remove(self, purchase_id: Purchase.id) -> None:
        pass

    def update(self, purchase: Purchase) -> None:
        pass