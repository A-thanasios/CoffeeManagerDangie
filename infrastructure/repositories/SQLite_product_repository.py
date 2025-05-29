from Module.interfaces.repository import Repository

from infrastructure.database.SQlite.operations.SQLite_product_operations import (
    insert_product,
    get_product_by_id,
    get_products_by_person_id,
    get_all_products,
    delete_product_by_id,
    update_product,
)


class SQLiteProductRepository(Repository):
    def __init__(self, db_path):
        self.db_path = db_path

    def add(self, product):
        return insert_product(self.db_path, product)

    def get_by_id(self, product_id):
        return get_product_by_id(self.db_path, product_id)

    def get_by_other_id(self, person_id):
        return get_products_by_person_id(self.db_path, person_id)

    def get_all(self):
        return get_all_products(self.db_path)

    def remove_by_id(self, product_id):
        return delete_product_by_id(self.db_path, product_id)

    def update(self, product):
        return update_product(self.db_path, product)