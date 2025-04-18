import os.path
from datetime import datetime

from database.db_setup import init_db
from database.operations.db_coffee_operations import insert_coffee, get_coffee_by_id
from database.operations.db_person_operations import insert_person, get_person_by_id
from database.operations.db_purchase_operations import insert_purchase, get_purchase_by_id
from src.data.coffee import Coffee
from src.data.person import Person
from src.data.purchase import Purchase
from src.data.structs.name import Name


def main():
    # Set the path for the database
    db_path = os.path.join('database', 'coffee_manager.db')


    # Check if the database file exists, if not, initialize it
    if not os.path.exists(db_path):
        init_db(db_path)


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


    person.id = insert_person(db_path, person)
    print(get_person_by_id(db_path, person.id))
    person1.id = insert_person(db_path, person1)
    print(get_person_by_id(db_path, person1.id))
    coffee.id = insert_coffee(db_path, coffee)
    print(get_coffee_by_id(db_path, coffee.id))
    purchase.id = insert_purchase(db_path, purchase)
    print(get_purchase_by_id(db_path, purchase.id))
    print(get_purchase_by_id(db_path, purchase.id).cost_by_one_person(person))

if __name__ == "__main__":
    main() 