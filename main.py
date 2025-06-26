import os
import sys
from PyQt6.QtWidgets import QApplication

import Configuration.settings

from Infrastructure import DatabaseFactory, RepositoryFactory
from Module import PersonService, PurchaseService
from Module.services.product_service import ProductService
from Module.services.strategy_executor import StrategyExecutor
from View.main_window import MainWindow

os.environ['QT_QPA_PLATFORM'] = Configuration.settings.environ_platform





def main():

    # Initialize the database
    db = DatabaseFactory.create_database()

    # Initialize the repositories
    person_repository =  RepositoryFactory(db).create_person_repository()
    product_repository =  RepositoryFactory(db).create_product_repository()
    purchase_repository =  RepositoryFactory(db).create_purchase_repository()

    # Initialize the services
    person_service = PersonService(person_repository)
    product_service = ProductService(product_repository)
    strategy_service = StrategyExecutor()
    purchase_service = PurchaseService(purchase_repository,
                                       product_service,
                                       person_service,
                                       strategy_service)


    # Initialize the gui
    app = QApplication(sys.argv)

    window = MainWindow(person_service, purchase_service)

    window.show()

    app.exec()


if __name__ == "__main__":
    main()
