from module.data.person import Person
from module.interfaces.cost_strategy import CostStrategy
from module.interfaces.repository import Repository


class AppService:
    def __init__(self, person_repo: Repository,
                 product_repo: Repository,
                 purchase_repo: Repository,
                 total_day_cost_by_person_strategy: CostStrategy):
        self.person_repo = person_repo
        self.product_repo = product_repo
        self.purchase_repo = purchase_repo
        self.total_day_cost_by_person_strategy = total_day_cost_by_person_strategy


