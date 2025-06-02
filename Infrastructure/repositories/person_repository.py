from MVP.Module.interfaces import PersonOperations
from MVP.Module.interfaces import Repository

from MVP.Module import Person

class SQLitePersonRepository(Repository):
    def __init__(self, db_path):
        self.db_path = db_path
        self.person_operations = PersonOperations()

    def create(self, person) -> int | TypeError | Exception:
        try:
            if not isinstance(person, Person):
                return TypeError("Expected a Person instance, got {type(person).__name__}")

            return self.person_operations.insert_person(self.db_path, person)

        except Exception as e:
            return Exception(f"Error while inserting person: {e}")

    def get_by_id(self, person_id) -> Person | None | TypeError | Exception:
        try:
            if not isinstance(person_id, int):
                return TypeError("Expected an integer for person_id, got {type(person_id).__name__}")

            return self.person_operations.get_person_by_id(self.db_path, person_id)
        except Exception as e:
            return Exception(f"Error while retrieving person by ID: {e}")

    def get_by_other_id(self, purchase_id) -> list[Person] | None | TypeError | Exception:
        try:
            if not isinstance(purchase_id, int):
                return TypeError("Expected an integer for purchase_id, got {type(purchase_id).__name__}")

            return self.person_operations.get_persons_by_purchase_id(self.db_path, purchase_id)
        except Exception as e:
            return Exception(f"Error while retrieving persons by purchase ID: {e}")

    def get_all(self) -> list[Person] | None | TypeError | Exception:
        try:
            return self.person_operations.get_all_persons(self.db_path)
        except Exception as e:
            return Exception(f"Error while retrieving all persons: {e}")

    def delete_by_id(self, person_id) -> bool | TypeError | Exception:
        try:
            if not isinstance(person_id, int):
                return TypeError("Expected an integer for person_id, got {type(person_id).__name__}")

            return self.person_operations.delete_person_by_id(self.db_path, person_id)

        except Exception as e:
            return Exception(f"Error while deleting person by ID: {e}")

    def update(self, person):
        try:
            if not isinstance(person, Person):
                return TypeError("Expected a Person instance, got {type(person).__name__}")

            return self.person_operations.update_person(self.db_path, person)

        except Exception as e:
            return Exception(f"Error while updating person: {e}")