class Product:
    def __init__(self, brand_name: str, shop: str, cost: int, db_id: int = None):
        if not isinstance(brand_name, str) or brand_name == '':
            raise ValueError("brand_name must be a non-empty string")
        if not isinstance(shop, str) or shop == '':
            raise ValueError("shop must be a non-empty string")
        if not isinstance(cost, (int, float)) or cost <= 0:
            raise ValueError(f"{cost} is not valid value. Cost must be a positive number")
        if db_id is not None and (not isinstance(db_id, int) or db_id < 0):
            raise ValueError("ID must be a positive integer or None")

        self.__id = db_id
        self.__brand_name = brand_name
        self.__shop = shop
        self.__cost = cost

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
    def brand_name(self):
        return self.__brand_name


    @property
    def shop(self):
        return self.__shop


    @property 
    def cost(self):
        return self.__cost


    def __str__(self):
        return f"{self.__brand_name} from {self.__shop}, cost= {self.__cost}"
        