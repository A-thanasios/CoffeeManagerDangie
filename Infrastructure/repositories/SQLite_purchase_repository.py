from Module.Interfaces import Repository
from Infrastructure.database.SQlite.operations import SQLite_purchase_operations
from Module import Purchase


class SQLitePurchaseRepository(Repository):
    def __init__(self, db_path):
        self.db_path = db_path
        self.purchase_operations = SQLite_purchase_operations

    def create(self, purchase: Purchase) -> int:
        if not isinstance(purchase, Purchase):
            raise TypeError(f"Expected a Purchase instance, got {type(purchase).__name__}")
        return self.purchase_operations.insert_purchase(self.db_path, purchase)

    def read_by_id(self, purchase_id: int) -> Purchase | None:
        if not isinstance(purchase_id, int):
            raise TypeError(f"Expected an integer for purchase_id, got {type(purchase_id).__name__}")
        return self.purchase_operations.select_purchase_by_id(self.db_path, purchase_id)

    def read_by_other_id(self, person_id: int) -> list[Purchase] | None:
        if not isinstance(person_id, int):
            raise TypeError(f"Expected an integer for person_id, got {type(person_id).__name__}")
        return self.purchase_operations.select_purchases_by_person_id(self.db_path, person_id)

    def read_all(self) -> list[Purchase] | None:
        return self.purchase_operations.select_all_purchases(self.db_path)

    def delete_by_id(self, purchase_id: int) -> bool:
        if not isinstance(purchase_id, int):
            raise TypeError(f"Expected an integer for purchase_id, got {type(purchase_id).__name__}")
        return self.purchase_operations.delete_purchase_by_id(self.db_path, purchase_id)

    def update(self, purchase: Purchase) -> bool:
        if not isinstance(purchase, Purchase):
            raise TypeError(f"Expected a Purchase instance, got {type(purchase).__name__}")
        return self.purchase_operations.update_purchase(self.db_path, purchase)
