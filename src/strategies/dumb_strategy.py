from .base import BaseStrategy


class DumbStrategy(BaseStrategy):
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
