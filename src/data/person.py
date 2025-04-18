from src.data.structs.name import Name


class Person:
    def __init__(self, name: Name, days_per_week: int, is_buying :bool= True, img: str='', db_id: int=None):
        self.__id = db_id
        self.__name = name
        self.__days_per_week = days_per_week
        self.__is_buying = is_buying
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
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, Name):
            raise ValueError("Name must be a Name object")
        self.__name = value

    @property
    def days_per_week(self):
        return self.__days_per_week

    @days_per_week.setter
    def days_per_week(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("days_per_week must be a positive integer")
        if value > 5:
            raise ValueError('days_per_week must be number between 0-5')
        self.__days_per_week = value

    @property
    def is_buying(self):
        return self.__is_buying

    @is_buying.setter
    def is_buying(self, value):
        if not isinstance(value, bool):
            raise ValueError("is_buying must be a boolean")
        self.__is_buying = value

    @property
    def img(self):
        return self.__img

    @img.setter
    def img(self, value):
        self.__img = value

    def __str__(self):
        return f"{self.__name.first_name} {self.__name.middle_name} {self.__name.last_name}"