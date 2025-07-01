from Module.Interfaces.strategy_service import StrategyService
from Infrastructure.factories.strategy_factory import StrategyFactory
from Module.model.person import Person
from Module.strategies.strategy_type import StrategyType


class StrategyExecutor(StrategyService):
    def __init__(self) -> None:

        self.strategy = None


    def calculate_costs(self,strategy, **kwargs ) -> list[tuple[Person, float]]:
        """Calculates the costs based on the given strategy.

            Args:
                strategy: Chosen strategy type for calculation.
                **kwargs: Keyword arguments to be passed to the strategy's calculate method.

            Returns:
                A dictionary containing the calculated costs.

            Raises:
                ValueError: If the number of arguments is incorrect or if the arguments are invalid.
            """
        if not isinstance(strategy, StrategyType):
            raise TypeError("strategy must be an instance of StrategyType")
        self.strategy = StrategyFactory.create_strategy(strategy)
        if not isinstance(kwargs, dict):
            raise TypeError("kwargs must be a dictionary")
        if len(kwargs) != self.strategy.arg_count():
            raise ValueError("Incorrect number of arguments")
        if not all(arg in self.strategy.arg_names() for arg in kwargs):
            raise ValueError(f"Invalid arguments. Expected: {self.strategy.arg_names()}")

        return self.strategy.calculate(**kwargs)


