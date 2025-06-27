from abc import ABC, abstractmethod


class CRUDService(ABC):
    @abstractmethod
    def create(self, *args, **kwargs) -> int | object:
        """
        create an object to the database.
        """
        pass

    @abstractmethod
    def read(self, obj_id: int) -> dict[str: any]:
        """
        read an object from the database by its ID and returns it as a dictionary where a key is attribute as string.
        """
        pass

    @abstractmethod
    def read_all(self) -> list[dict[str, any]]:
        """
        Read all objects from the database and returns a list of dictionary where a key is attribute as string.
        """
        pass
    @abstractmethod
    def remove(self, obj_id: int) -> None:
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

    def get_object(self, obj_id: int) -> object:
        """
        Read an object from the database by its ID and return an object as a model
        """