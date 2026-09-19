from abc import ABC, abstractmethod


class BaseStrategy(ABC):
    """
    Abstract base class for trading strategies.
    """
    def __init__(self, ticker):
        self.ticker = ticker

    @abstractmethod
    def deposit(self, date):
        """
        Determines how much to deposit in the account on a given date.
        Args :
        - date: datetime.date | The date for which to evaluate the deposit.
        """
        return 0

    @abstractmethod
    def decision(self, price):
        """
        Determines the trading decision based on the current price.
        Args :
        - price: float | The current price of the stock.
        Returns :
        - decision: str | The trading decision ("Buy", "Sell", or "Hold").
        - percentage: float | The percentage of the account's balance to use for the decision.
        """
        pass

    @abstractmethod
    def total_invested(self):
        """
        Returns the total amount of money invested by the strategy.
        """
        pass