class Account :
    def __init__(self, initial_balance=0):
        self.balance = initial_balance
        self.positions = {} # {ticker1 : qty , ticker2 : qty , ...}

    def deposit(self, amount):
        """
        Deposits a specified amount into the account balance.
        Args:
        - amount: float | The amount to deposit.
        """
        self.balance += amount

    def add_position(self, symbol, quantity, current_price):
        """
        Buys a specified quantity of a position and adds it to the portfolio.
        Args:
        - symbol: str | The symbol of the position to add.
        - quantity: float | The quantity of the position to add.
        - current_price: float | The current price of the position.
        """
        amount = quantity*current_price
        if amount <= 0 or self.balance < amount:
            pass
        else:
            if symbol in self.positions:
                self.positions[symbol] += quantity
            else:
                self.positions[symbol] = quantity
            self.balance -= amount

    def sell_position(self, symbol, quantity, current_price):
        """
        Sells a specified quantity of a position in the portfolio.
        Args:
        - symbol: str | The symbol of the position to sell.
        - quantity: float | The quantity of the position to sell.
        - current_price: float | The current price of the position.
        """
        amount = quantity * current_price
        if symbol in self.positions:
            if quantity > self.positions[symbol]:
                raise ValueError(f"Cannot sell {quantity} of {symbol}. Only {self.positions[symbol]} available.")
            else:
                self.positions[symbol] -= quantity
                self.balance += amount
                if self.positions[symbol] <= 0:
                    del self.positions[symbol]
        else:
            pass

