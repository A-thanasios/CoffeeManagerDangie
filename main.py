import os
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QMainWindow

from view.main_window import MainWindow

os.environ['QT_QPA_PLATFORM'] = 'xcb'

from infrastructure.factories.database_factory import DatabaseFactory
from infrastructure.factories.repository_factory import RepositoryFactory
from module.services.strategy_service import StrategyService
from module.services.person_service import PersonService
from module.services.purchase_service import PurchaseService
from module.strategies.by_person_strategy import ByPersonStrategy


def main():

    # Initialize the database
    db = DatabaseFactory.create_database()

    # Initialize the repositories
    person_repository =  RepositoryFactory(db).create_person_repository()
    product_repository =  RepositoryFactory(db).create_product_repository()
    purchase_repository =  RepositoryFactory(db).create_purchase_repository()

    # Initialize the services
    purchase_service = PurchaseService(purchase_repository)
    person_service = PersonService(person_repository, purchase_service)
    app_service = StrategyService(person_service, purchase_service, product_repository, ByPersonStrategy())

    # Initialize the gui
    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    app.exec()


if __name__ == "__main__":
    main()
