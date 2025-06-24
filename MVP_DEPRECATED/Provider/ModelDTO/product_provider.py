from MVP_DEPRECATED.Provider.dto.product_dto import ProductDTO
from MVP_DEPRECATED.Module.Interfaces import Provider


class ProductProvider(Provider):
    def __init__(self, product_service) -> None:
        self.product_service = product_service

    def add(self, new_product: ProductDTO) -> None:
        self.product_service.create(**new_product.model.dump())

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



    def update(self, product_id: str, updated_data: list[dict]) -> None:
        pass

    def delete(self, product_id: str) -> None:
        pass