from Module.Interfaces import CRUDService, Repository
from Module.model.purchase import Purchase


class PaymentService(CRUDService):
    def __init__(self, repository: Repository):
        self.repo = repository

    def create(self, purchase: Purchase) -> int | object:
        if not isinstance(purchase, Purchase):
            raise TypeError("Invalid argument type: purchase")
        return self.repo.create(purchase)

    def read(self, purchase_id: int) -> dict[str: any]:
        """
        returns a dictionary with the given purchase id as a key and the qr_codes path as value, both str
        """
        if not isinstance(purchase_id, int):
            raise TypeError("Invalid argument type: purchase_id")
        return self.repo.read_by_id(purchase_id)

    def read_all(self) -> list[dict[str, any]]:
        raise NotImplementedError("Use read(purchase_id) instead.")

    def update(self, purchase_id) -> None:
        #TODO: Refactoring would be needed
        self.repo.update(purchase_id)

    def delete(self, purchase_id: int) -> None:
        #TODO: Refactoring would be needed
        self.repo.delete_by_id(purchase_id)