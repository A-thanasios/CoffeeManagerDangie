from module.interfaces.repository import Repository

from infrastructure.database.operations.db_coffee_operations import (
    insert_coffee,
    get_coffee_by_id,
    get_coffees_by_person_id,
    get_all_coffees,
    delete_coffee_by_id,
    update_coffee,
)


class SQLiteCoffeeRepository(Repository):
    def __init__(self, db_path):
        self.db_path = db_path

    def add(self, coffee):
        return insert_coffee(self.db_path, coffee)

    def get_by_id(self, coffee_id):
        return get_coffee_by_id(self.db_path, coffee_id)

    def get_by_other_id(self, person_id):
        return get_coffees_by_person_id(self.db_path, person_id)

    def get_all(self):
        return get_all_coffees(self.db_path)

    def remove_by_id(self, coffee_id):
        return delete_coffee_by_id(self.db_path, coffee_id)

    def update(self, coffee):
        return update_coffee(self.db_path, coffee)