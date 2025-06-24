from abc import ABC, abstractmethod


class Provider(ABC):
    @abstractmethod
    def add(self, item: object) -> bool:
        """add a new item."""
        pass
    @abstractmethod
    def get(self, item_id: str|list[str]) -> object | list[object]:
        """Get an item by its ID."""
        pass
    @abstractmethod
    def update(self, item_id: str, updated_data: list[dict]) -> bool:
        """Update an existing item."""
        pass
    @abstractmethod
    def delete(self, item_id: str) -> bool:
        """Delete an item by its ID."""
        pass
