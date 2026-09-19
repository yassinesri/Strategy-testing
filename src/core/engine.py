import src.core.portfolio as portfolio
import pandas as pd

def simulate_a_strategy(a_strategy, data, *args):
    """
    Simulates a given strategy on historical data.
    Args :
    - a_strategy: function | The strategy function to simulate.
    - data: DataFrame | The historical data to simulate the strategy on.
    - *args: Additional arguments to pass to the strategy function.
    """

    an_account = portfolio.Account()
    a_strategy_instance = a_strategy(*args)
    worth_history = []
    nav_history = []

    nav = 100.0
    shares_outstanding = 0.0

    for t in range(len(data)):
        current_data = data.iloc[t:t+1]
        price = float(current_data.iloc[0])
        date = current_data.index[0].date()

        # Adding money to the account
        amount_to_deposit = a_strategy_instance.deposit(date)
        an_account.deposit(amount_to_deposit)
        shares_outstanding += amount_to_deposit / nav

        # Making a decision based on the strategy
        decision, percentage = a_strategy_instance.decision(price)

        # Executing the decision
        if decision == "Buy":
            quantity_to_buy = an_account.balance * (percentage / 100) / price
            an_account.add_position(current_data.name, quantity_to_buy, price)
        elif decision == "Sell":
            quantity_to_sell = an_account.positions.get(current_data.name, 0) * (percentage / 100)
            an_account.sell_position(current_data.name, quantity_to_sell, price)
        elif decision == "Hold":
            pass

        # Recording the total worth of the account
        current_worth = an_account.balance + sum(an_account.positions.values())*price
        worth_history.append(current_worth)

        if shares_outstanding > 0:
            nav = current_worth / shares_outstanding
        nav_history.append(nav)

    worth_history = pd.Series(worth_history, index=data.index)

    return worth_history, nav_history
