from src.structs.name import Name


class Person:
    def __init__(self, name: Name, days_per_week: int, img: str=''):
        self.__name = name
        self.__days_per_week = days_per_week
        self.__img = img

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
    def img(self):
        return self.__img

    @img.setter
    def img(self, value):
        self.__img = value