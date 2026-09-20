from typing import Type

from src.strategies.base import BaseStrategy
from src.strategies.buy_and_hold import BuyAndHold
from src.strategies.mean_reversion import MeanReversion
from src.strategies.moving_average_crossover import MovingAverageCrossover
from src.strategies.test import TestStrategy


STRATEGIES: dict[str, Type[BaseStrategy]] = {
	"buy_and_hold": BuyAndHold,
	"mean_reversion": MeanReversion,
	"moving_average_crossover": MovingAverageCrossover,
	"test_strategy": TestStrategy,
}


def load_strategy(strategy_name: str) -> Type[BaseStrategy]:
	"""Return the strategy class matching the supplied name."""
	try:
		return STRATEGIES[strategy_name]
	except KeyError as error:
		valid_strategies = ", ".join(STRATEGIES)
		raise ValueError(
			f"Unknown strategy '{strategy_name}'. Choose one of: {valid_strategies}."
		) from error