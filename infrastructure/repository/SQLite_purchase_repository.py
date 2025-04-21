from infrastructure.database.SQLite_db_setup import db_path

from infrastructure.repository.repository import Repository
from infrastructure.database.operations.db_purchase_operations import insert_purchase, get_purchase_by_id, \
    get_purchases_by_person_id, get_all_purchases, update_purchase, delete_purchase_by_id

db_path = db_path

class SQLitePurchaseRepository(Repository):

    def add(self, purchase):
        return insert_purchase(db_path, purchase)

    def get_by_id(self, purchase_id):
        return get_purchase_by_id(db_path, purchase_id)

    def get_by_other_id(self, person_id):
        return get_purchases_by_person_id(db_path, person_id)

    def get_all(self):
        return get_all_purchases(db_path)

    def remove_by_id(self, purchase_id):
        return delete_purchase_by_id(db_path, purchase_id)

    def update(self, purchase):
        return update_purchase(db_path, purchase)

