from Module import Product
from Module import Person
from Module.Interfaces import CostStrategy


class ByPersonStrategy(CostStrategy):

    def calculate(self, products: list[Product], persons: list[Person]) -> list[tuple[Person]]:
        costs = []
        cost_sum = self.__cost_sum(products)
        total_days_sum = self.__total_days_sum(persons)

        for person in persons:
            costs.append(tuple([person, self.calculate_person(person, cost_sum, total_days_sum)]))

        return costs

    @staticmethod
    def calculate_person(person: Person, cost_sum, total_days_sum) -> float:
        if person.detail.days_per_week == 0:
            raise ValueError('Person has no days per week')

        if total_days_sum <= 0:
            raise ValueError('No days sum available')

        return cost_sum * (person.detail.days_per_week / total_days_sum)



    @staticmethod
    def __total_days_sum(persons: list[Person]):
        days_sum = 0

        for person in persons:
            days_sum += person.detail.days_per_week

        return days_sum


    @staticmethod
    def __cost_sum(products: list[Product]) -> float:
        cost_sum = 0

        for product in products:
            cost_sum += product.cost

        return cost_sum

    def arg_count(self) -> int:
        return len(self.arg_names())

    def arg_names(self) -> list[str]:
        return ["products", "persons"]