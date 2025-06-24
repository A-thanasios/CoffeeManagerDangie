from abc import ABC, abstractmethod


class StrategyService(ABC):
    @abstractmethod
    def calculate_costs(self, **kwargs) -> dict:
        """
        Calculate costs for each person for the given products by chosen strategy.
        """