from abc import ABC, abstractmethod


class Provider(ABC):
    @abstractmethod
    def get(self, item_id: str|list[str]) -> object:
        """Get an item by its ID."""
        pass
    @abstractmethod
    def create(self, item: object) -> None:
        """Create a new item."""
        pass
    @abstractmethod
    def update(self, item_id: str, updated_data: list[dict]) -> None:
        """Update an existing item."""
        pass
    @abstractmethod
    def delete(self, item_id: str) -> None:
        """Delete an item by its ID."""
        pass
