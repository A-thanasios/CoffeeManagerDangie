class Product:
    def __init__(self, brand_name: str, shop: str, cost: int, img: str='', db_id: int = None):
        if not isinstance(brand_name, str) or brand_name == '':
            raise ValueError("brand_name must be a non-empty string")
        if not isinstance(shop, str) or shop == '':
            raise ValueError("shop must be a non-empty string")
        if not isinstance(cost, (int, float)) or cost < 0:
            raise ValueError("cost must be a positive number")
        if db_id is not None and (not isinstance(db_id, int) or db_id < 0):
            raise ValueError("ID must be a positive integer or None")
        if img is not None and not isinstance(img, str):
            raise ValueError("img must be a string or None")

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

    @brand_name.setter
    def brand_name(self, value):
        if not isinstance(value, str):
            raise ValueError("brand_name must be a string")
        self.__brand_name = value

    @property
    def shop(self):
        return self.__shop

    @shop.setter
    def shop(self, value):
        if not isinstance(value, str):
            raise ValueError("shop must be a string")
        self.__shop = value

    @property 
    def cost(self):
        return self.__cost

    @cost.setter
    def cost(self, value):
        if not isinstance(value, (int, float)) or value < 0:
            raise ValueError("cost must be a positive number")
        self.__cost = value
    
    @property
    def img(self):
        return self.__img

    @img.setter
    def img(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("img must be a string or None")
        self.__img = value







    def __str__(self):
        return f"{self.__brand_name} from {self.__shop}, cost= {self.__cost}"
        