from abc import ABC, abstractmethod

class Repository(ABC):
    """
    Abstract base class for repositories.
    """

    @abstractmethod
    def create(self, entity) -> int | Exception:
        """
        Add an entity to the repositories.
        """
        pass

    @abstractmethod
    def get_by_id(self, entity_id) -> object | Exception:
        """
        Get an entity from the repositories by its ID.
        """
        pass

    @abstractmethod
    def get_by_other_id(self, other_id) -> object | Exception:
        """
        Get an entity from the repositories by ID from another entity.
        """
        pass

    @abstractmethod
    def get_all(self) -> list[object] | Exception:
        """
        Get all entities from the repositories.
        """
        pass

    @abstractmethod
    def delete_by_id(self, entity_id) -> bool | Exception:
        """
        Remove an entity from the repositories by its ID.
        """
        pass

    @abstractmethod
    def update(self, entity) -> bool | Exception:
        """
        Update an existing entity in the repositories.
        """
        pass