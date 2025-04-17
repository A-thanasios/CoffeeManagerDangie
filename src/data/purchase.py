from datetime import datetime

from src.data.coffee import Coffee
from src.data.person import Person


class Purchase:
    def __init__(self, name: str, persons: list[Person], coffees: list[Coffee], date: datetime, db_id: int = None):
        self.__id = db_id
        self.__name = name
        self.__persons = persons
        self.__coffees = coffees
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

    @property
    def persons(self):
        return self.__persons

    @property
    def coffees(self):
        return self.__coffees

    @property
    def date(self):
        return self.__date

    @date.setter
    def date(self, value):
        self.__date = value

    def __str__(self):
        return f"Purchase(id={self.__id}, name={self.__name}, persons={self.__persons}, coffees={self.__coffees}, date={self.__date})"
