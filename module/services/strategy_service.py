from module.interfaces.cost_strategy import CostStrategy
from module.interfaces.crud_service import CRUDService
from module.interfaces.repository import Repository


class StrategyService:
    def __init__(self, person_service: CRUDService,
                 purchase_service: CRUDService,
                 product_repo: Repository,
                 by_person_strategy: CostStrategy):
        self.person_service = person_service
        self.purchase_service = purchase_service
        self.product_repo = product_repo
        self.by_person_strategy = by_person_strategy


    def calculate_person_costs(self, person_id: int, purchase_id: int) -> float:
        # verify if person already exists
        person = self.person_service.get(person_id)

        # verify if person has relation to purchase


        # if yes calculate costs
        # else return error

    def calculate_purchase_costs(self, purchase):
        pass
        # verify if purchase already exists
        # verify if purchase has any products
        # verify if purchase has any persons
        # if yes calculate costs
        # else return error