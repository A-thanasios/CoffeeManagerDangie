import os.path
from datetime import datetime

from infrastructure.factories.database_factory import DatabaseFactory
from infrastructure.factories.repository_factory import RepositoryFactory
from infrastructure.repositories.SQLite_product_repository import SQLiteProductRepository
from infrastructure.repositories.SQLite_person_repository import SQLitePersonRepository
from infrastructure.repositories.SQLite_purchase_repository import SQLitePurchaseRepository

from module.services.app_service import AppService


def main():

    # Initialize the database
    db = DatabaseFactory.create_database()

    # Initialize the repositories
    person_repository =  RepositoryFactory(db).create_person_repository()
    product_repository =  RepositoryFactory(db).create_product_repository()
    purchase_repository =  RepositoryFactory(db).create_purchase_repository()

    # Initialize the services
    app = AppService(person_repository, product_repository, purchase_repository)


if __name__ == "__main__":
    main() 