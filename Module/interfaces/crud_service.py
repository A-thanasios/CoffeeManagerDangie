from abc import ABC, abstractmethod

from Module.interfaces.repository import Repository


class CRUDService(ABC):
    @abstractmethod
    def add(self, obj) -> int:
        """
        Add an object to the database.
        """
        pass

    @abstractmethod
    def get(self, obj_id) -> object:
        """
        Get an object from the database by its ID.
        """
        pass
    @abstractmethod
    def get_all(self) -> list[object]:
        """
        Get all objects from the database.
        """
        pass
    @abstractmethod
    def remove(self, obj_id) -> None:
        """
        Remove an object from the database by its ID.
        """
        pass
    @abstractmethod
    def update(self, obj) -> None:
        """
        Update an existing object in the database.
        """
        pass