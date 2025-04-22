import os.path
from datetime import datetime

from infrastructure.factories.databasefactory import DatabaseFactory
from infrastructure.repositories.SQLite_coffee_repository import SQLiteCoffeeRepository
from infrastructure.repositories.SQLite_person_repository import SQLitePersonRepository
from infrastructure.repositories.SQLite_purchase_repository import SQLitePurchaseRepository
from module.Strategies.total_day_cost_by_person import TotalDayCostByPerson
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

    purchase_repo = SQLitePurchaseRepository(db.path)
    person_repo = SQLitePersonRepository(db.path)
    coffee_repo = SQLiteCoffeeRepository(db.path)
    cost_by_person = TotalDayCostByPerson()

    person_id = person_repo.add(person)

    person1_id = person_repo.add(person1)

    coffee_id = coffee_repo.add(coffee)

    purchase_id = purchase_repo.add(purchase)

    print(purchase_repo.get_by_id(purchase_id))
    print(person_repo.get_by_id(person_id))
    print(coffee_repo.get_all)

    for purchase in purchase_repo.get_all():
        print(purchase)

    print(cost_by_person.calculate(purchase, person))

if __name__ == "__main__":
    main() 