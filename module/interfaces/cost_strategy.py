from abc import ABC, abstractmethod

class CostStrategy(ABC):
    @abstractmethod
    def calculate(self, purchase, person):
        pass