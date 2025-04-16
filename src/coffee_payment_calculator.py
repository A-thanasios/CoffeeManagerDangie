from src.data.coffee import Coffee
from src.data.person import Person
from src.data.purchase import Purchase


class CoffeePaymentCalculator:
    def __init__(self):
        self.__days_sum = None

    def cost_by_one_person(self, purchase: Purchase, coffee: Coffee, person: Person):
        if not self.__days_sum:
            self.__total_days_sum(purchase.persons)
        if self.__days_sum <= 0:
            raise ValueError('No days sum available')
        
        return (coffee.cost * person.days_per_week) / self.__days_sum

    def __total_days_sum(self, persons: list[Person]):
        self.__days_sum = 0

        for person in persons:
            self.__days_sum += person.days_per_week