from abc import ABC, abstractmethod

class CostStrategy(ABC):
    @abstractmethod
    def calculate(self, **kwargs) -> dict:
        """Calculate strategy"""
        pass

    def arg_count(self) -> int:
        """returns the number of arguments required by the strategy"""
        pass

    def arg_names(self) -> list[str]:
        """returns the names of the arguments required by the strategy"""
        pass