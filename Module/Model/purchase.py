from Module.Model.product import Product
from Module.Model.person import Person
from Module.Model.data.purchase_detail import PurchaseDetail
from Module.Model.data.purchase_settlement import PurchaseSettlement


class Purchase:
    def __init__(self,
                 purchase_settlements: list[tuple],
                 products: list[Product],
                 db_id: int = None,
                 **detail_args):

        # Detail validation
        if len(detail_args) < PurchaseDetail.__field_count__():
            raise ValueError(f"Expected {PurchaseDetail.__field_count__()} arguments, got {len(detail_args)}")

        # Purchase settlements validation
        if len(purchase_settlements) == 0:
            raise ValueError("purchase_settlements list cannot be empty")

        for ps in purchase_settlements:
            if not isinstance(ps, tuple):
                raise ValueError(f"Each settlement must be a tuple, got {type(ps).__name__}")
            if len(ps) not in (2, 3):
                raise ValueError("Settlement tuple must have 2 or 3 elements")
            if not isinstance(ps[0], Person):
                raise ValueError(f"First element must be Person, got {type(ps[0]).__name__}")
            if not isinstance(ps[1], (int, float)):
                raise ValueError(f"Second element must be number, got {type(ps[1]).__name__}")
            if len(ps) == 3 and not isinstance(ps[2], bool):
                raise ValueError(f"Third element must be boolean, got {type(ps[2]).__name__}")

        # Products validation
        if len(products) == 0:
            raise ValueError("products list cannot be empty")
        if (not isinstance(products, list)
                or not all(isinstance(product, Product) for product in products)):
            raise ValueError("products must be a list of Product objects")

        # ID validation
        if db_id is not None and (not isinstance(db_id, int) or db_id < 0):
            raise ValueError("ID must be a positive integer or None")



        
        self.__id = db_id
        self.__purchase_detail = PurchaseDetail(**detail_args)
        self.__purchase_settlements = [PurchaseSettlement(*settlement) for settlement in purchase_settlements]
        self.__persons = [purchase_settlement.person for purchase_settlement in self.__purchase_settlements]
        self.__products = products




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
    def detail(self) -> PurchaseDetail:
        return self.__purchase_detail

    @property
    def purchase_detail_dict(self) -> dict[str: any]:
        return {
                "name":self.__purchase_detail.name,
                "date": self.__purchase_detail.date
                }

    @property
    def purchase_settlements(self) -> list[PurchaseSettlement]:
        return self.__purchase_settlements

    @property
    def purchase_settlements_dict(self) -> list[dict]:
        return [{
            "person": purchase_settlement.person,
            "amount": purchase_settlement.amount,
            "is_paid": purchase_settlement.is_paid
                } for purchase_settlement in self.__purchase_settlements]

    @property
    def detail_field_count(self):
        return self.__purchase_detail.__field_count__()
    @property
    def settlement_field_count(self):
        """
        Return: the number of fields in the purchase settlements
        """
        return PurchaseSettlement.__field_count__()

    def __eq__(self, other):
        return isinstance(other, Purchase) and self.detail.name == other.detail.name
