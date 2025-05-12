from module.dto.purchase_dto import PurchaseDTO
from module.interfaces.Provider import Provider
from module.model.purchase import Purchase


class PurchaseProvider(Provider):
    def __init__(self, purchase_service, person_service, product_service) -> None:
        self.purchase_service = purchase_service
        self.person_service = person_service
        self.product_service = product_service

    def get(self, item_id: str | list[str]) -> object:
        if not item_id:
            purchases = self.purchase_service.get_all()
            if not purchases:
                return []
            else:
                ls = []
                for purchase in purchases:
                    ls.append(PurchaseDTO(
                        id=purchase.id,
                        name=purchase.name,
                        persons_id= [person.id for person in purchase.persons],
                        products_id=[product.id for product in purchase.products],
                        date=purchase.date
                    ))

                return ls
        else:
            purchase = self.purchase_service.get(item_id)
            return PurchaseDTO(
                id=purchase.id,
                name=purchase.name,
                persons_id=[person.id for person in purchase.persons],
                products_id=[product.id for product in purchase.products],
                date=purchase.date
            )

    def create(self, new_purchase: PurchaseDTO) -> None:
        persons  = []
        for person_id in new_purchase.persons_id:
            person = self.person_service.get(person_id)
            persons.append(person)

        products = []
        for product_id in new_purchase.products_id:
            product = self.product_service.get_by_id(product_id)
            products.append(product)

        self.purchase_service.add(Purchase(new_purchase.name,
                                              persons,
                                               products,
                                               new_purchase.date))

    def update(self, item_id: str, updated_data: dict) -> None:
        purchase = self.purchase_service.get(item_id)
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

        self.purchase_service.update(purchase)

    def delete(self, item_id: str | list[str]) -> None:
        self.purchase_service.remove(item_id)