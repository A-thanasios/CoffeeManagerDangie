from datetime import datetime

from module.data.product import Product
from module.data.person import Person


class Purchase:
    def __init__(self, name: str, persons: list[Person], products: list[Product], date: datetime, db_id: int = None):
        self.__id = db_id
        self.__name = name
        self.__persons = persons
        self.__products = products
        self.__date = date


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
        if not isinstance(value, str) or not value:
            raise ValueError("Name must be a non-empty string")
        self.__name = value

    @property
    def persons(self):
        return self.__persons

    @property
    def products(self):
        return self.__products

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        self.__date = value

    def __str__(self):
        return (f"Purchase(id={self.__id}, "
                f"name={self.__name}, "
                f"persons={list(person.__str__() for person in self.__persons)}, "
                f"products={list(product.__str__() for product in self.__products)}, "
                f"date={self.__date})")
