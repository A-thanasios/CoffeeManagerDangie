from MVP.Module.model.person import Person
from MVP.Module import Purchase
from MVP.Module.interfaces.crud_service import CRUDService
from MVP.Module.interfaces.repository import Repository
from MVP.Module.services.purchase_service import PurchaseService


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

        return self.repo.create(person)

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
            return []

        return lst

    def get_all_purchases(self, person_id) -> list[Purchase]:
        if not isinstance(person_id, int) or person_id < 0:
            raise ValueError("ID must be a positive integer")

        persons = self.purchase_service.get_all_persons(person_id)

        if not persons:
            raise ValueError("No persons found")

        person_purchases = [self.purchase_service.get(p)
                            for p in persons if p.id == person_id]

        if not person_purchases:
            raise ValueError("No purchases found for this person")

        return person_purchases

    def remove(self, person_id) -> None:
        if not isinstance(person_id, int) or person_id < 0:
            raise ValueError("ID must be a positive integer")
        if not self.repo.get_by_id(person_id):
            raise ValueError("Person not found")
        if self.purchase_service.person_has_purchases(person_id):
            raise ValueError("Person has purchases, cannot delete")

        self.repo.delete_by_id(person_id)

    def update(self, person) -> None:
        if not isinstance(person, Person):
            raise ValueError("arg must be a Person object")
        if not self.repo.get_by_id(person.id):
            raise ValueError("Person not found")

        self.repo.update(person)