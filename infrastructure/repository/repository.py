from abc import ABC, abstractmethod

class Repository(ABC):
    """
    Abstract base class for a repository.
    """

    @abstractmethod
    def add(self, entity):
        """
        Add an entity to the repository.
        """
        pass

    @abstractmethod
    def get_by_id(self, entity_id):
        """
        Get an entity from the repository by its ID.
        """
        pass

    @abstractmethod
    def get_by_other_id(self, other_id):
        """
        Get an entity from the repository by ID from another entity.
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Get all entities from the repository.
        """
        pass

    @abstractmethod
    def remove_by_id(self, entity_id):
        """
        Remove an entity from the repository by its ID.
        """
        pass

    @abstractmethod
    def update(self, entity):
        """
        Update an existing entity in the repository.
        """
        pass