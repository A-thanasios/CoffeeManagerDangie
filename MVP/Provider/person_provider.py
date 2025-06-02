from MVP.Module.dto.person_dto import PersonDTO
from MVP.Module.interfaces import Provider
from MVP.Module import Person
from MVP.Module import PersonDetail


class PersonProvider(Provider):
    def __init__(self, person_service) -> None:
        self.person_service = person_service

    def get(self, item_id: str | list[str]) -> PersonDTO|list[PersonDTO]:
        if not item_id:
            persons = self.person_service.get_all()
            if not persons:
                return []
            else:
                ls = []

            for person in persons:
                ls.append(PersonDTO(
                    id=person.id,
                    first_name=person.name.first_name,
                    last_name=person.name.last_name,
                    middle_name=person.name.middle_name,
                    days_per_week=person.days_per_week,
                    is_buying=person.is_buying,
                    img=person.img
                ))

            return ls
        else:
            person = self.person_service.get(item_id)
            return PersonDTO(
                id=person.id,
                first_name=person.name.first_name,
                last_name=person.name.last_name,
                middle_name=person.name.middle_name,
                days_per_week=person.days_per_week,
                is_buying=person.is_buying,
                img=person.img
            )

    def create(self, new_person: PersonDTO) -> None:
        name = PersonDetail(new_person.first_name, new_person.last_name, new_person.middle_name)
        person = Person(name, new_person.days_per_week, new_person.is_buying, new_person.img)
        self.person_service.create(person)

    def update(self, person_id: str, updated_data: dict) -> None:
        person = self.person_service.get(person_id)
        for key, value in updated_data.items():
            if 'name' in key:
                setattr(person.name, key, value)
            else:
                setattr(person, key, value)

        self.person_service.update(person)

    def delete(self, item_id: str) -> None:
        self.person_service.remove(item_id)