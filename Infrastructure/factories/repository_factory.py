from Module.Interfaces.database import Database
from Infrastructure.repositories.SQLite_person_repository import SQLitePersonRepository
from Infrastructure.repositories.SQLite_product_repository import SQLiteProductRepository
from Infrastructure.repositories.SQLite_purchase_repository import SQLitePurchaseRepository
from Module.Interfaces.repository import Repository


class RepositoryFactory:
    def __init__(self, database: Database):
        self.db = database

    def create_person_repository(self) -> Repository:
        if self.db.type == 'sqlite':
            return SQLitePersonRepository(self.db.path)
        else:
            raise ValueError(f"Unsupported repository type: {self.db.type}")

    def create_product_repository(self) -> Repository:
        if self.db.type == 'sqlite':
            return SQLiteProductRepository(self.db.path)
        else:
            raise ValueError(f"Unsupported repository type: {self.db.type}")

    def create_purchase_repository(self) -> Repository:
        if self.db.type == 'sqlite':
            return SQLitePurchaseRepository(self.db.path)
        else:
            raise ValueError(f"Unsupported repository type: {self.db.type}")