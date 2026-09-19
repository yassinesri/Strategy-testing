from .base import BaseStrategy


class MeanReversion(BaseStrategy):
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
