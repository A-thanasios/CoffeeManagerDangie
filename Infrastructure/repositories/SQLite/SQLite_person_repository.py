from Infrastructure.database.SQlite.operations import SQLite_person_operations
from Module.Interfaces import Repository

from Module import Person

class SQLitePersonRepository(Repository):
    def create(self, person: Person) -> int:
        if not isinstance(person, Person):
            raise TypeError("Expected a Person instance, got {type(person).__name__}")

        return self._operations.insert_person(self.db_path, person)

    def read_by_id(self, person_id: int) -> Person | None:
        if not isinstance(person_id, int):
            raise TypeError("Expected an integer for person_id, got {type(person_id).__name__}")

        return self._operations.select_person_by_id(self.db_path, person_id)

    def read_by_other_id(self, purchase_id: int) -> list[Person] | None:
        if not isinstance(purchase_id, int):
            raise TypeError("Expected an integer for purchase_id, got {type(purchase_id).__name__}")

        return self._operations.select_persons_by_purchase_id(self.db_path, purchase_id)


    def read_all(self) -> list[Person] | None:
            return self._operations.select_all_persons(self.db_path)

    def delete_by_id(self, person_id: int) -> bool:
        if not isinstance(person_id, int):
            raise TypeError("Expected an integer for person_id, got {type(person_id).__name__}")

        return self._operations.delete_person_by_id(self.db_path, person_id)

    def update(self, person: Person):
        if not isinstance(person, Person):
            raise TypeError("Expected a Person instance, got {type(person).__name__}")

        return self._operations.update_person(self.db_path, person)

    def _get_operations(self):
        return SQLite_person_operations
