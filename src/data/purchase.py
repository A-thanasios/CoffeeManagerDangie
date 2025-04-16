from datetime import datetime

from src.data.coffee import Coffee
from src.data.person import Person


class Purchase:
            def __init__(self, name: str, persons: list[Person], coffee: Coffee, date: datetime):
                self.__name = name
                self.__persons = persons
                self.__coffee = coffee
                self.__date = date

            @property
            def name(self):
                return self.__name

            @property
            def persons(self):
                return self.__persons

            @property
            def coffee(self):
                return self.__coffee

            @property
            def date(self):
                return self.__date

            @date.setter
            def date(self, value):
                self.__date = value