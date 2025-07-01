from Module.Interfaces import CRUDService
from Module import Product


class ProductService(CRUDService):
    def __init__(self, repo) -> None:
        self.repo = repo

    def create(self, *args) -> Product:
        # Create Product object and returns it.
        # This method does not save the object to the database.
        # Life cycle of this object is managed by Purchase object

        return Product(*args, db_id=None)

    def read(self, product_id) -> object:
        if not isinstance(product_id, int) or product_id < 0:
            raise ValueError("ID must be a positive integer")

        product = self.repo.get_by_id(product_id)
        if not product:
            raise ValueError("Product not found")

        return product

    def read_all(self) -> list[object]:
        lst = self.repo.get_all()

        if not lst:
            return []

        return lst

    def delete(self, product_id) -> None:
        if not isinstance(product_id, int) or product_id < 0:
            raise ValueError("ID must be a positive integer")
        if not self.repo.get_by_id(product_id):
            raise ValueError("Product not found")

        self.repo.delete_by_id(product_id)

    def update(self, product) -> None:
        if not isinstance(product, Product):
            raise ValueError("arg must be a Product object")
        if not self.repo.get_by_id(product.id):
            raise ValueError("Product not found")

        self.repo.update(product)

    def get_object(self, product_id: int) -> Product:
        if not isinstance(product_id, int) or product_id < 0:
            raise ValueError("ID must be a positive integer")

        product: Product = self.repo.read_by_id(product_id)
        if not product:
            raise ValueError("Product not found")
        return product