from abc import ABC, abstractmethod

class Repository(ABC):
    """
    Abstract base class for repositories.
    """
    def __init__(self, db_path, repository=None):
        self.db_path = db_path
        self._operations = self._get_operations()
        self.aux_repo = repository

    @abstractmethod
    def create(self, entity) -> int | Exception:
        """
        Add an entity to the repositories.
        """
        pass

    @abstractmethod
    def read_by_id(self, entity_id) -> object:
        """
        Get an entity from the repositories by its ID.
        """
        pass

    @abstractmethod
    def read_by_other_id(self, other_id) -> object | Exception:
        """
        Get an entity from the repositories by ID from another entity.
        """
        pass

    @abstractmethod
    def read_all(self) -> list[object] | Exception:
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

    @abstractmethod
    def _get_operations(self):
        """
        Returns the operation class for the repository.
        """
        pass

    # TODO: _validate_type(self, value: Any, expected_type: Type, param_name: str) -> None:
    '''if not isinstance(value, expected_type):
        raise TypeError(f"Expected {expected_type.__name__} for {param_name}, got {type(value).__name__}")'''

