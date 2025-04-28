from module.data.person import Person
from module.data.purchase import Purchase
from module.interfaces.cost_strategy import CostStrategy


class ByPersonStrategy(CostStrategy):
    def calculate(self, purchase: Purchase, person: Person):
        if person.days_per_week == 0:
            raise ValueError('Person has no days per week')

        days_sum = self.__total_days_sum(purchase.persons)

        if days_sum <= 0:
            raise ValueError('No days sum available')

        return self.__cost_sum(purchase) * (person.days_per_week / days_sum)

    def calculate_all(self, purchase: Purchase):
        costs = {}
        for person in purchase.persons:
            costs[person] = self.calculate(purchase, person)

        return costs

    @staticmethod
    def __total_days_sum(persons: list[Person]):
        days_sum = 0

        for person in persons:
            days_sum += person.days_per_week

        return days_sum


    @staticmethod
    def __cost_sum(purchase: Purchase):
        if len(purchase.products) == 1:
            return purchase.products[0].cost

        cost_sum = 0

        for product in purchase.products:
            cost_sum += product.cost

        return cost_sum