class Account :
    def __init__(self, initial_balance):
        self.balance = initial_balance
        self.positions = {}

    def deposit(self, amount):
        """
        Deposits a specified amount into the account balance.
        Args:
        - amount: float | The amount to deposit.
        """
        self.balance += amount

    def add_position(self, symbol, quantity):
        """
        Buys a specified quantity of a position and adds it to the portfolio.
        Args:
        - symbol: str | The symbol of the position to add.
        - quantity: float | The amount of money to invest in the position.
        """
        if self.balance < quantity:
            raise ValueError("Insufficient balance to add position")
        else:
            if symbol in self.positions:
                self.positions[symbol] += quantity
            else:
                self.positions[symbol] = quantity
            self.balance -= quantity

    def sell_position(self, symbol, amount):
        """
        Sells a specified quantity of a position in the portfolio.
        Args:
        - symbol: str | The symbol of the position to sell.
        - amount: float | The amount of the position to sell.
        """
        if symbol in self.positions:
            if amount > self.positions[symbol]:
                raise ValueError(f"Cannot sell {amount} of {symbol}. Only {self.positions[symbol]} available.")
            else:
                self.positions[symbol] -= amount
                self.balance += amount
                if self.positions[symbol] <= 0:
                    del self.positions[symbol]
        else:
            raise ValueError(f"No position for symbol: {symbol}")

    def update_positions(self, new_prices):
        """
        Updates the price of every position in the portfolio
        Args:
        - new_prices: dict | A dictionary where keys are symbols and values are the new prices.
        """
        for symbol, new_price in new_prices.items():
            if symbol in self.positions:
                # Update the value of the position based on the new price
                self.positions[symbol] = new_price
            else:
                raise ValueError(f"No position for symbol: {symbol}")