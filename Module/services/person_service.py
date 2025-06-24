from Module.Model.person import Person
from Module.Interfaces.crud_service import CRUDService
from Module.Interfaces.repository import Repository



class PersonService(CRUDService):
    def __init__(self, repo: Repository) -> None:
        self.repo = repo


    def create(self, **kwargs) -> int:
        person = Person(**kwargs)
        persons = self.repo.read_all()
        if persons:
            for p in persons:
                if p == person:
                    raise ValueError("Person already exists")
        return self.repo.create(person)

    def read(self, person_id: int) -> dict[str: any]:
        if not isinstance(person_id, int) or person_id < 0:
            raise ValueError("ID must be a positive integer")

        person: Person = self.repo.read_by_id(person_id)
        if not person:
            raise ValueError("Person not found")

        return {"id": person.id, **person.person_detail_dict}

    def read_all(self) -> dict[int: dict[str: any]]:
        lst = self.repo.read_all()
        p_dict = {}

        if not lst:
            return []

        for p in lst:
            p_dict[p.id] = (self.read(p.id))

        return p_dict



    def remove(self, person_id) -> None:
        if not isinstance(person_id, int) or person_id < 0:
            raise ValueError("ID must be a positive integer")
        if not self.repo.read_by_id(person_id):
            raise ValueError("Person not found")

        self.repo.delete_by_id(person_id)

    def update(self,person_id, **kwargs) -> None:
        if not kwargs:
            raise ValueError("No arguments provided for update")
        if not isinstance(person_id, int) or person_id < 0:
            raise ValueError("Person ID must be a positive integer")
        person: Person = self.repo.read_by_id(person_id)

        if not person:
            raise ValueError("Person not found")

        if len(kwargs) > person.detail_field_count:
            raise ValueError(f"Expected {person.detail_field_count} arguments, got {len(kwargs)}")

        for item, value in kwargs.items():
            try:
                setattr(person.detail, item, value)
            except AttributeError:
                raise ValueError(f"Invalid argument: {item}")

        self.repo.update(person)