from module.model.person import Person
from module.model.purchase import Purchase
from module.interfaces.repository import Repository
from module.services.person_service import PersonService
from module.services.purchase_service import PurchaseService
from module.strategies.by_person_strategy import ByPersonStrategy


class StrategyService:
    def __init__(self, person_service: PersonService,
                 purchase_service: PurchaseService,
                 product_repo: Repository,
                 by_person_strategy: ByPersonStrategy):

        self.person_service = person_service
        self.purchase_service = purchase_service
        self.product_repo = product_repo
        self.by_person_strategy = by_person_strategy


    def calculate_person_costs(self, person_id: int) -> dict[Purchase, float]:
        # verify if person already exists
        person = self.person_service.get(person_id)
        if not person:
            raise ValueError("Person not found")

        # verify if person has relation to purchases
        if not self.purchase_service.person_has_purchases(person_id):
            raise ValueError("Person has no purchases")

        purchases_lst = self.person_service.get_all_purchases(person_id)
        purchases_costs_dict = {}

        for purchase in purchases_lst:
            cost = self.by_person_strategy.calculate(purchase, person)
            purchases_costs_dict[purchase] = cost

        return purchases_costs_dict


    def calculate_purchase_costs(self, purchase_id) -> dict[Person, float]:
        # verify if purchase already exists
        purchase = self.purchase_service.get(purchase_id)
        if not purchase:
            raise ValueError("Purchase not found")

        # verify if purchase has any persons
        if not self.purchase_service.get_all_persons(purchase_id):
            raise ValueError("Purchase has no persons")

        # if yes calculate costs
        return self.by_person_strategy.calculate_all(purchase)
        # else return error