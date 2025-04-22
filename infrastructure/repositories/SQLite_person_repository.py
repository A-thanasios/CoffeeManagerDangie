from module.interfaces.repository import Repository

from infrastructure.database.operations.db_person_operations import (
    insert_person,
    get_person_by_id,
    get_persons_by_purchase_id,
    get_all_persons,
    delete_person_by_id,
    update_person
)


class SQLitePersonRepository(Repository):
    def __init__(self, db_path):
        self.db_path = db_path

    def add(self, person):
        return insert_person(self.db_path, person)

    def get_by_id(self, person_id):
        return get_person_by_id(self.db_path, person_id)

    def get_by_other_id(self, purchase_id):
        return get_persons_by_purchase_id(self.db_path, purchase_id)

    def get_all(self):
        return get_all_persons(self.db_path)

    def remove_by_id(self, person_id):
        return delete_person_by_id(self.db_path, person_id)

    def update(self, person):
        return update_person(self.db_path, person)