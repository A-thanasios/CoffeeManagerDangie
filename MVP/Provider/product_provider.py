from MVP.Module import ProductDTO
from MVP.Module.interfaces import Provider
from MVP.Module import Product


class ProductProvider(Provider):
    def __init__(self, product_service) -> None:
        self.product_service = product_service

    def get(self, product_id: str | list[str]) -> object:
        if not product_id:
            products = self.product_service.get_all()
            if not products:
                return []
            else:
                ls = []
                for product in products:
                    ls.append(ProductDTO(
                        id=product.id,
                        name=product.name,
                        shop=product.shop,
                        cost= product.price
                    ))
                return ls
        else:
            product = self.product_service.get_by_id(product_id)
            return ProductDTO(
                        id=product.id,
                        name=product.name,
                        shop=product.shop,
                        cost= product.price
                    )

    def create(self, product: ProductDTO) -> int:
        return self.product_service.create(Product(
            product.name,
            product.shop,
            product.cost
        ))

    def update(self, product_id: str, updated_data: list[dict]) -> None:
        pass

    def delete(self, product_id: str) -> None:
        pass