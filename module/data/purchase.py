from datetime import datetime

from module.data.product import Product
from module.data.person import Person


class Purchase:
    def __init__(self, name: str, persons: list[Person], products: list[Product], date: datetime, db_id: int = None):
        if not isinstance(name, str) or not name:
            raise ValueError("Name must be a non-empty string")
        if not isinstance(persons, list) or not all(isinstance(person, Person) for person in persons):
            raise ValueError("persons must be a list of Person objects")
        if not isinstance(products, list) or not all(isinstance(product, Product) for product in products):
            raise ValueError("products must be a list of Product objects")
        if not isinstance(date, datetime):
            raise ValueError("date must be a datetime object")
        if db_id is not None and (not isinstance(db_id, int) or db_id < 0):
            raise ValueError("ID must be a positive integer or None")
        if len(persons) == 0:
            raise ValueError("persons list cannot be empty")
        
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
