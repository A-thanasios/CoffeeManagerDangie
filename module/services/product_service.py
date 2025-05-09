from module.interfaces.crud_service import CRUDService
from module.model.product import Product


class ProductService(CRUDService):
    def __init__(self, repo) -> None:
        self.repo = repo

    def add(self, product) -> int:
        if not isinstance(product, Product):
            raise ValueError("arg must be a Product object")

        return self.repo.add(product)

    def get(self, product_id) -> object:
        if not isinstance(product_id, int) or product_id < 0:
            raise ValueError("ID must be a positive integer")

        product = self.repo.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found")

        return product

    def get_all(self) -> list[object]:
        lst = self.repo.get_all()

        if not lst:
            return []

        return lst

    def remove(self, product_id) -> None:
        if not isinstance(product_id, int) or product_id < 0:
            raise ValueError("ID must be a positive integer")
        if not self.repo.get_by_id(product_id):
            raise ValueError("Product not found")

        self.repo.remove_by_id(product_id)

    def update(self, product) -> None:
        if not isinstance(product, Product):
            raise ValueError("arg must be a Product object")
        if not self.repo.get_by_id(product.id):
            raise ValueError("Product not found")

        self.repo.update(product)