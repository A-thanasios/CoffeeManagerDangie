class Coffee:
    def __init__(self, brand_name: str, shop: str, cost: int, img: str='', db_id: int = None):
        self.__id = db_id
        self.__brand_name = brand_name
        self.__shop = shop
        self.__cost = cost
        self.__img = img

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
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
    
    @property
    def img(self):
        return self.__img

    @brand_name.setter
    def brand_name(self, value):
        if not isinstance(value, str):
            raise ValueError("brand_name must be a string")
        self.__brand_name = value

    @shop.setter
    def shop(self, value):
        if not isinstance(value, str):
            raise ValueError("shop must be a string")
        self.__shop = value

    @cost.setter
    def cost(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("cost must be a positive number")
        self.__cost = value
        