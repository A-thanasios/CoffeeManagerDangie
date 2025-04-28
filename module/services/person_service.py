from module.data.person import Person
from module.interfaces.crud_service import CRUDService
from module.interfaces.repository import Repository
from module.services.purchase_service import PurchaseService


class PersonService(CRUDService):
    def __init__(self, repo: Repository, purchase_service: PurchaseService) -> None:
        self.repo = repo
        self.purchase_service = purchase_service

    def add(self, person) -> Person.id:
        if not isinstance(person, Person):
            raise ValueError("arg must be a Person object")

        persons = self.repo.get_all()
        for p in persons:
            if p.name == person.name:
                raise ValueError("Person already exists")

        return self.repo.add(person)

    def get(self, person_id) -> Person:
        if not isinstance(person_id, int) or person_id < 0:
            raise ValueError("ID must be a positive integer")

        person = self.repo.get_by_id(person_id)
        if not person:
            raise ValueError("Purchase not found")

        return person

    def get_all(self) -> list[Person]:
        lst = self.repo.get_all()

        if not lst:
            raise ValueError("No persons found")

        return lst

    def remove(self, person_id) -> None:
        if not isinstance(person_id, int) or person_id < 0:
            raise ValueError("ID must be a positive integer")
        if not self.repo.get_by_id(person_id):
            raise ValueError("Person not found")
        if self.purchase_service.person_has_purchases(person_id):
            raise ValueError("Person has purchases, cannot delete")

        self.repo.remove_by_id(person_id)

    def update(self, person) -> None:
        if not isinstance(person, Person):
            raise ValueError("arg must be a Person object")
        if not self.repo.get_by_id(person.id):
            raise ValueError("Person not found")

        self.repo.update(person)