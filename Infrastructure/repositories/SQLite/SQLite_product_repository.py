from Module.Interfaces import Repository
from Infrastructure.database.SQlite.operations import SQLite_product_operations
from Module import Product


class SQLiteProductRepository(Repository):
# TODO: Refactor product coupling
    def create(self, product: Product, purchase_id: int) -> int:
        if not isinstance(product, Product):
            raise TypeError(f"Expected a Product instance, got {type(product).__name__}")
        if not isinstance(purchase_id, int):
            raise TypeError(f"Expected an integer for purchase_id, got {type(purchase_id).__name__}")
        return self._operations.insert_product(self.db_path, product, purchase_id)

    def read_by_id(self, product_id: int) -> Product | None:
        if not isinstance(product_id, int):
            raise TypeError(f"Expected an integer for product_id, got {type(product_id).__name__}")
        return self._operations.select_product_by_id(self.db_path, product_id)

    def read_by_other_id(self, purchase_id: int) -> list[Product] | None:
        if not isinstance(purchase_id, int):
            raise TypeError(f"Expected an integer for purchase_id, got {type(purchase_id).__name__}")
        return self._operations.select_products_by_purchase_id(self.db_path, purchase_id)

    def read_all(self) -> list[Product] | None:
        return self._operations.select_all_products(self.db_path)

    def update(self, product: Product) -> bool:
        if not isinstance(product, Product):
            raise TypeError(f"Expected a Product instance, got {type(product).__name__}")
        return self._operations.update_product(self.db_path, product)

    def delete_by_id(self, product_id: int) -> bool:
        if not isinstance(product_id, int):
            raise TypeError(f"Expected an integer for product_id, got {type(product_id).__name__}")
        return self._operations.delete_product_by_id(self.db_path, product_id)

    def _get_operations(self):
        return SQLite_product_operations
