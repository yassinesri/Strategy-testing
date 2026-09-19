from .base import BaseStrategy


class MovingAverageCrossover(BaseStrategy):
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
