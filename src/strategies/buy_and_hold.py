from .base import BaseStrategy

class BuyAndHold(BaseStrategy):
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
