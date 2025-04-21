from datetime import datetime

from module.data.coffee import Coffee
from module.data.person import Person


class Purchase:
    def __init__(self, name: str, persons: list[Person], coffees: list[Coffee], date: datetime, db_id: int = None):
        self.__id = db_id
        self.__name = name
        self.__persons = persons
        self.__coffees = coffees
        self.__date = date

    def cost_by_one_person(self, person: Person):
        days_sum = self.__total_days_sum(self.persons)

        if days_sum <= 0:
            raise ValueError('No days sum available')

        return (self.__cost_sum() * person.days_per_week) / days_sum

    def __total_days_sum(self, persons: list[Person]):
        days_sum = 0

        for person in persons:
            days_sum += person.days_per_week

        return days_sum

    def __cost_sum(self):
        if len(self.coffees) == 1:
            return self.coffees[0].cost

        cost_sum = 0

        for coffee in self.coffees:
            cost_sum += coffee.cost

        return cost_sum

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
