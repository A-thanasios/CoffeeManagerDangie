import os.path
from datetime import datetime

from infrastructure.factory.databasefactory import DatabaseFactory
from infrastructure.repository.SQLite_purchase_repository import SQLitePurchaseRepository
from module.data.coffee import Coffee
from module.data.person import Person
from module.data.purchase import Purchase
from module.data.structs.name import Name


def main():

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

    db = DatabaseFactory.create_database()

    if not db.exists():
        db.init_db()

    purchase_repository = SQLitePurchaseRepository(db.path)

    purchase_id = purchase_repository.add(purchase)
    print(purchase_repository.get_by_id(purchase_id))

if __name__ == "__main__":
    main() 