from Module.strategies.strategy_type import StrategyType
from Module.strategies.by_person_strategy import ByPersonStrategy


class StrategyFactory:
    @staticmethod
    def create_strategy(strategy_type):
        if strategy_type == StrategyType.ByPerson:
            return ByPersonStrategy()

        raise ValueError(f"Unsupported strategy type: {strategy_type}")