from MVP_DEPRECATED.Provider.dto.product_dto import ProductDTO
from MVP_DEPRECATED.Provider.dto.purchase_dto import PurchaseDTO
from MVP_DEPRECATED.Module.Interfaces import Provider, CRUDService
from MVP_DEPRECATED.Module.Model import Purchase


class PurchaseProvider(Provider):
    def __init__(self, purchase_service: CRUDService, person_service: CRUDService, product_service: CRUDService) -> None:
        self.purchase_service = purchase_service
        self.person_service = person_service
        self.product_service = product_service

    def add(self, new_purchase: PurchaseDTO, new_products: list[ProductDTO]) -> bool:
        products = []

        if new_purchase.products_id not in new_products:
            raise ValueError("Products_id doesn't match")

        for product in new_products:
            if product.id in new_purchase.products_id:
                products.append(tuple(*product))
            else:
                raise ValueError(f"Product with id {product.id} not found in provided products")

        self.purchase_service.create(new_purchase.name, new_purchase.date,
                                              person_ids=new_purchase.persons_id,
                                              products=products,
                                              strategy_type=new_purchase.strategy_type)
        return True

    def get(self, purchase_id: str | list[str]) -> PurchaseDTO | list[PurchaseDTO]:
        if not purchase_id:
            # If no item_id is provided, return all purchases
            purchases = self.purchase_service.read_all()
            if not purchases:
                return []
            else:
                ls = []
                for purchase in purchases:
                    ls.append(self.__create_PurchaseDTO(purchase))

                return ls
        elif isinstance(purchase_id, list):
            # If a list of item_ids is provided, return purchases for those ids
            purchases = []
            for p_id in purchase_id:
                purchase = self.purchase_service.read(p_id)
                if purchase:
                    purchases.append(self.__create_PurchaseDTO(purchase))
            return purchases
        else:
            purchase = self.purchase_service.read(purchase_id)
            if purchase:
                return self.__create_PurchaseDTO(purchase)

        raise Exception(f"Purchase with id {purchase_id} not found")



    def update(self, purchase_id: str, updated_data: dict) -> bool:
        purchase = self.purchase_service.read(purchase_id)
        for key, value in updated_data.items():
            if 'persons' in key:
                persons = []
                for person_id in value:
                    person = self.person_service.get(person_id)
                    persons.append(person)
                setattr(purchase, key, persons)

            elif 'products' in key:
                products = []
                for product_id in value:
                    product = self.product_service.get(product_id)
                    products.append(product)
                setattr(purchase, key, products)

            else:
                setattr(purchase, key, value)
                

        return self.purchase_service.update(purchase)

    def delete(self, purchase_id: str | list[str]) -> bool:
        self.purchase_service.remove(purchase_id)


    @staticmethod
    def __create_PurchaseDTO(purchase: dict[str: any]) -> PurchaseDTO:
        return PurchaseDTO(
            id=purchase['id'],
            name=purchase['name'],
            settlements=purchase['settlements'],
            products_id=purchase['products'],
            date=purchase['date']
        )