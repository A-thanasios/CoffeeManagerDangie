from MVP.Module.model.product import Product
from MVP.Module.model.person import Person
from MVP.Module.model.data.purchase_detail import PurchaseDetail
from MVP.Module.model.data.purchase_settlement import PurchaseSettlement


class Purchase:
    def __init__(self, purchase_detail: PurchaseDetail,
                 persons: list[Person],
                 products: list[Product],
                 purchase_settlements: list[PurchaseSettlement],
                 db_id: int = None):
        if not isinstance(purchase_detail, PurchaseDetail):
            raise ValueError("purchase_detail must be a valid PurchaseDetail object")
        if (not isinstance(persons, list)
                or not all(isinstance(person, Person) for person in persons)):
            raise ValueError("persons must be a list of Person objects")
        if (not isinstance(products, list)
                or not all(isinstance(product, Product) for product in products)):
            raise ValueError("products must be a list of Product objects")
        if not isinstance(purchase_detail, PurchaseDetail):
            raise ValueError("purchase_detail must be a valid PurchaseDetail object")
        if (not isinstance(purchase_settlements, list)
                or not all(isinstance(ps, PurchaseSettlement) for ps in purchase_settlements)):
            raise ValueError("purchase_settlements must be a list of PurchaseSettlement objects")

        if db_id is not None and (not isinstance(db_id, int) or db_id < 0):
            raise ValueError("ID must be a positive integer or None")
        if len(persons) == 0:
            raise ValueError("persons list cannot be empty")
        if len(products) == 0:
            raise ValueError("products list cannot be empty")
        if len(purchase_settlements) == 0:
            raise ValueError("purchase_settlements list cannot be empty")
        if len(persons) != len(purchase_settlements):
            raise ValueError("The number of persons must match the number of purchase settlements")
        if [ps for ps in purchase_settlements if ps.person not in persons]:
            raise ValueError("All PurchaseSettlements must reference a Person in the persons list")

        
        self.__id = db_id
        self.__purchase_detail = purchase_detail
        self.__persons = persons
        self.__products = products
        self.__purchase_settlements = purchase_settlements


    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if self.__id:
            raise ValueError("ID is already set and cannot be changed")

        if not isinstance(value, int) or value < 0:
            raise ValueError("ID must be a positive integer")
        self.__id = value

    @property
    def persons(self):
        return self.__persons

    @property
    def products(self):
        return self.__products

    @property
    def purchase_detail(self):
        return self.__purchase_detail

    @property
    def purchase_settlements(self):
        return self.__purchase_settlements
