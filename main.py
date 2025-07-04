import os
import sys
from PyQt6.QtWidgets import QApplication

import Configuration.settings

from Infrastructure import DatabaseFactory, RepositoryFactory
from Infrastructure.utilities.mail_sending.auth2_gmail_send.gmail_send import send_email
from Module import PersonService, PurchaseService
from Module.services.mail_service import MailService
from Module.services.payment_service import PaymentService
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
    qr_code_repository = RepositoryFactory(db).create_qr_code_repository(purchase_repository)

    # Initialize the services
    person_service = PersonService(person_repository)
    product_service = ProductService(product_repository)
    strategy_service = StrategyExecutor()
    payment_service = PaymentService(qr_code_repository)
    purchase_service = PurchaseService(purchase_repository,
                                       product_service,
                                       person_service,
                                       payment_service,
                                       strategy_service)

    mail_service = MailService(purchase_service, payment_service)


    # Initialize the gui
    app = QApplication(sys.argv)

    window = MainWindow(person_service,
                        purchase_service,
                        payment_service,
                        mail_service)

    window.show()

    app.exec()


if __name__ == "__main__":
    main()
