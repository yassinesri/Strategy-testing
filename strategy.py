from abc import ABC, abstractmethod
import indicators


class Base_Strategy(ABC):
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

class buy_and_hold(Base_Strategy):
    """
    Simple buy and hold strategy, can be used to benchmark the performance of other strategies.
    """
    def __init__(self,ticker, amount_to_invest_monthly):
        """
        Args :
        - ticker: str | The stock ticker symbol.
        - amount_to_invest_monthly: float | The amount of money to invest each month
        """
        super().__init__(ticker)
        self.amount_to_invest_monthly = amount_to_invest_monthly
        self.months_invested = []

    def deposit(self, date):
        """
        Decides how much to deposit in the account
        Args : 
        - date: datetime.date | The date for which to evaluate the deposit.
        """
        if date.month not in self.months_invested:  
            self.months_invested.append(date.month)
            return self.amount_to_invest_monthly
        else :
            return 0
        
    def decision(self, price):
        """
        Returns a decision : buying with 100% of the account's balance when possible
        Args :
        - price: float | The current price of the stock.
        """
        return "Buy", 100

    def total_invested(self):
        """
        Returns the total amount of money invested by the strategy.
        """
        return self.amount_to_invest_monthly * len(self.months_invested)

class dumb_strategy(Base_Strategy):
    """
    - Investing a specified amount of money each month
    - Manages each stock a on daily basis : if the price goes up for 3 days in a row, it buys the stock
    """
    def __init__(self,ticker, amount_to_invest_monthly):
        """
        Args :
        - ticker: str | The stock ticker symbol.
        - amount_to_invest_monthly: float | The amount of money to invest each month
        """
        super().__init__(ticker)
        self.amount_to_invest_monthly = amount_to_invest_monthly
        self.months_invested = []
        self.price_history = []

    def deposit(self, date):
        """
        Decides how much to deposit in the account
        Args : 
        - date: datetime.date | The date for which to evaluate the deposit.
        """
        if date.month not in self.months_invested:  
            self.months_invested.append(date.month)
            return self.amount_to_invest_monthly
        else :
            return 0
        
    def decision(self, price):
        """
        Returns a decision : buying with 100% of the account's balance, selling 100% of the position, or holding.
        Args :
        - price: float | The current price of the stock.
        """
        self.price_history.append(price)
        if len(self.price_history) > 3:
            self.price_history.pop(0)
        if len(self.price_history) < 3:
            return "Hold", 0
        if self.price_history[-3] < self.price_history[-2] and self.price_history[-2] < self.price_history[-1]:
            return "Buy", 100
        elif self.price_history[-3] > self.price_history[-2] and self.price_history[-2] > self.price_history[-1]:
            return "Sell", 100
        return "Hold", 0

    def total_invested(self):
        """
        Returns the total amount of money invested by the strategy.
        """
        return self.amount_to_invest_monthly * len(self.months_invested)


class moving_average_crossover(Base_Strategy):
    """
    A classic trend-following strategy used in institutional trading.
    It buys when a short-term moving average crosses above a long-term moving average,
    and sells when the opposite occurs.
    """
    def __init__(self, ticker, amount_to_invest_monthly, short_window=20, long_window=50):
        super().__init__(ticker)
        self.amount_to_invest_monthly = amount_to_invest_monthly
        self.months_invested = []
        self.short_window = short_window
        self.long_window = long_window
        self.price_history = []

    def deposit(self, date):
        if date.month not in self.months_invested:
            self.months_invested.append(date.month)
            return self.amount_to_invest_monthly
        return 0

    def decision(self, price):
        self.price_history.append(price)
        if len(self.price_history) < self.long_window:
            return "Hold", 0

        short_ma = sum(self.price_history[-self.short_window:]) / self.short_window
        long_ma = sum(self.price_history[-self.long_window:]) / self.long_window

        if short_ma > long_ma:
            return "Buy", 100
        elif short_ma < long_ma:
            return "Sell", 100
        return "Hold", 0

    def total_invested(self):
        return self.amount_to_invest_monthly * len(self.months_invested)


class mean_reversion(Base_Strategy):
    """
    A mean-reversion strategy commonly used in quantitative trading.
    It buys when price is far below a rolling average and sells when it is far above.
    """
    def __init__(self, ticker, amount_to_invest_monthly, window=20, threshold=0.02):
        super().__init__(ticker)
        self.amount_to_invest_monthly = amount_to_invest_monthly
        self.months_invested = []
        self.window = window
        self.threshold = threshold
        self.price_history = []

    def deposit(self, date):
        if date.month not in self.months_invested:
            self.months_invested.append(date.month)
            return self.amount_to_invest_monthly
        return 0

    def decision(self, price):
        self.price_history.append(price)
        if len(self.price_history) < self.window:
            return "Hold", 0

        window_prices = self.price_history[-self.window:]
        average_price = sum(window_prices) / len(window_prices)
        deviation = (price - average_price) / average_price

        if deviation < -self.threshold:
            return "Buy", 100
        elif deviation > self.threshold:
            return "Sell", 100
        return "Hold", 0

    def total_invested(self):
        return self.amount_to_invest_monthly * len(self.months_invested)
