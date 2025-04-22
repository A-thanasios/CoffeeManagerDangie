from module.data.person import Person
from module.data.purchase import Purchase
from module.interfaces.cost_strategy import CostStrategy


class TotalDayCostByPerson(CostStrategy):
    def calculate(self, purchase: Purchase, person: Person):
        days_sum = self.__total_days_sum(purchase.persons)

        if days_sum <= 0:
            raise ValueError('No days sum available')

        return self.__cost_sum(purchase) * (person.days_per_week / days_sum)

    @staticmethod
    def __total_days_sum(persons: list[Person]):
        days_sum = 0

        for person in persons:
            days_sum += person.days_per_week

        return days_sum


    @staticmethod
    def __cost_sum(purchase: Purchase):
        if len(purchase.coffees) == 1:
            return purchase.coffees[0].cost

        cost_sum = 0

        for coffee in purchase.coffees:
            cost_sum += coffee.cost

        return cost_sum