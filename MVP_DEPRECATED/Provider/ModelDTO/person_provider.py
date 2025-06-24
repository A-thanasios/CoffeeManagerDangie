from MVP_DEPRECATED.Provider.dto.person_dto import PersonDTO
from MVP_DEPRECATED.Module.Interfaces import Provider


class PersonProvider(Provider):
    def __init__(self, person_service) -> None:
        self.person_service = person_service

    def add(self, new_person: PersonDTO) -> None:
        person_data = new_person.model_dump()
        person_data.pop('id', None)
        self.person_service.create(**person_data)

    def get(self, person_id: str | list[str]= None) -> PersonDTO|list[PersonDTO]:
        if not person_id:
            persons = self.person_service.read_all()
            if not persons:
                return []
            else:
                ls = []

            for person_id, person_detail in persons.items():
                ls.append(PersonDTO.model_construct(**person_detail))

            return ls
        else:
            person = self.person_service.read(person_id)
            return PersonDTO.model_construct(id= person_id, **person.person_detail_dict)


    def update(self, person_id: str, updated_data: dict) -> None:
        self.person_service.update(person_id, **updated_data)

    def delete(self, item_id: str) -> None:
        self.person_service.remove(item_id)