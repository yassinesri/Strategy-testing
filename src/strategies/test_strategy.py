from .base import BaseStrategy


class TestStrategy(BaseStrategy):
    """
    This strategy sells when the price drops by more than a certain percentage during the day,
    and buys when the price increases by more than a certain percentage
    """
    def __init__(self, ticker, amount_to_invest_monthly, drop_threshold=0.02, rise_threshold=0.02):
        super().__init__(ticker)
        self.amount_to_invest_monthly = amount_to_invest_monthly
        self.months_invested = []
        self.price_history = []
        self.drop_threshold = drop_threshold
        self.rise_threshold = rise_threshold
        self.current_day = None
        self.day_reference_price = None
        self.lowest_price = None
        self.has_sold = False

    def deposit(self, date):
        if date != self.current_day:
            self.current_day = date
            self.day_reference_price = None
            self.lowest_price = None
            self.has_sold = False

        if date.month not in self.months_invested:
            self.months_invested.append(date.month)
            return self.amount_to_invest_monthly
        return 0

    def decision(self, price):
        self.price_history.append(price)

        if self.day_reference_price is None:
            self.day_reference_price = price

        if self.has_sold:
            self.lowest_price = min(self.lowest_price, price)
            if price >= self.lowest_price * (1 + self.rise_threshold):
                self.has_sold = False
                self.lowest_price = None
                return "Buy", 100
            return "Hold", 0

        if price <= self.day_reference_price * (1 - self.drop_threshold):
            self.has_sold = True
            self.lowest_price = price
            return "Sell", 100

        return "Hold", 0

    def total_invested(self):
        return self.amount_to_invest_monthly * len(self.months_invested)
