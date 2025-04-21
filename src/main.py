import os.path
from datetime import datetime

from gi.importer import repository

from infrastructure.database.SQLite_db_setup import init_db, db_exists
from infrastructure.database.operations.db_coffee_operations import insert_coffee, get_coffee_by_id
from infrastructure.database.operations.db_person_operations import insert_person, get_person_by_id
from infrastructure.database.operations.db_purchase_operations import insert_purchase, get_purchase_by_id
from infrastructure.repository.SQLite_purchase_repository import SQLitePurchaseRepository
from src.data.coffee import Coffee
from src.data.person import Person
from src.data.purchase import Purchase
from src.data.structs.name import Name


def main():
    # Set the path for the database
    db_path = os.path.join('database', 'coffee_manager.db')


    # Check if the database file exists, if not, initialize it
    if not db_exists():
        init_db()


    person = Person(
        Name('John', 'M.', 'Doe'),
        3,
        True,
        'https://example.com/image.jpg'
    )

    person1 = Person(
        Name('Alice', '', 'Wonderland'),
        5,
        True,
        'https://example.com/image.jpg'
    )

    coffee = Coffee('Costa',
                    'Costa Coffee',
                    250,
                    'https://example.com/coffee.jpg')

    purchase = Purchase(r'Costa/April/2023',
                        [person, person1],
                        [coffee],
                        datetime.now())


    purchase_repository = SQLitePurchaseRepository()

    purchase_id = purchase_repository.add(purchase)
    print(purchase_repository.get_by_id(purchase_id))

if __name__ == "__main__":
    main() 