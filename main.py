import os
import sys
from PyQt6.QtWidgets import QApplication

import Configuration.settings

from Infrastructure import DatabaseFactory, RepositoryFactory
from Module import PersonService, PurchaseService
from MVP_DEPRECATED.Provider import PersonProvider, PurchaseProvider, ProductProvider
from MVP_DEPRECATED.Provider.dto.person_dto import PersonDTO

os.environ['QT_QPA_PLATFORM'] = Configuration.settings.environ_platform





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
    #app_service = StrategyService(person_service, purchase_service, product_repository, ByPersonStrategy())

    # Initialize the providers
    person_provider = PersonProvider(person_service)
    purchase_provider = PurchaseProvider(purchase_service, person_service, product_repository)
    product_provider = ProductProvider(product_repository)


    #person_provider.add(PersonDTO(id= -1, name='Petr', e_mail='sis@oto.cz', days_per_week=5, is_buying=True))
    print(person_provider.get())

    '''# Initialize the gui
    app = QApplication(sys.argv)

    window = MainWindow(person_provider, purchase_provider, product_provider, app_service)

    window.show()

    app.exec()'''


if __name__ == "__main__":
    main()
