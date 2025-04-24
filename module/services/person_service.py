from module.data.person import Person
from module.interfaces.crud_service import CRUDService
from module.interfaces.repository import Repository


class PersonService(CRUDService):
    def __init__(self, repo: Repository) -> None:
        self.repo = repo

    def add(self, person) -> Person.id:
        return self.repo.add(person)

    def get(self, person_id) -> Person:
        return self.repo.get_by_id(person_id)

    def get_all(self) -> list[Person]:
        return self.repo.get_all()

    def remove(self, person_id) -> None:
        self.repo.remove_by_id(person_id)

    def update(self, person) -> None:
        self.repo.update(person)