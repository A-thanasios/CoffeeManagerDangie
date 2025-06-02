import sqlite3
from abc import ABC, abstractmethod

from MVP.Module import Person


class PersonOperations(ABC):
    @abstractmethod
    def insert_person(self, db_path: str, person: Person) -> int:
        """Insert a new person into the database.
        Args:
            db_path (str): The path to the database.
            person (object): The person object to insert.
        Returns:
            int: The ID of the inserted person.
        """
        pass

    @abstractmethod
    def get_person_by_id(self, db_path: str, person_id: int) -> Person | None:
        """Get a person by their ID.
        Args:
            db_path (str): The path to the database.
            person_id (int): The ID of the person to retrieve.
        Returns:
            object: The person object if found, otherwise None.
        """
        pass

    @abstractmethod
    def get_persons_by_purchase_id(self, db_path: str, purchase_id: int) -> list[Person]:
        """Get persons associated with a specific purchase ID.
        Args:
            db_path (str): The path to the database.
            purchase_id (int): The ID of the purchase.
        Returns:
            list[object]: A list of person objects associated with the purchase ID.
        """
        pass

    @abstractmethod
    def get_all_persons(self, db_path: str) -> list[Person] | None:
        """Get all persons from the database.
        Args:
            db_path (str): The path to the database.
        Returns:
            list[object]: A list of all person objects in the database.
        """
        pass

    @abstractmethod
    def update_person(self, db_path: str, person: object) -> bool | sqlite3.Error:
        """Update a person's details in the database.
        Args:
            db_path (str): The path to the database.
            person (object): The person object with updated details.
        Returns:
            bool: True if the update was successful, otherwise False.
        """
        pass

    @abstractmethod
    def delete_person_by_id(self, db_path: str, person_id: int) -> bool | sqlite3.Error:
        """Delete a person by their ID.
        Args:
            db_path (str): The path to the database.
            person_id (int): The ID of the person to delete.
        Returns:
            bool: True if the deletion was successful, otherwise False.
        """
        pass
