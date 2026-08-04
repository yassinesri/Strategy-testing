import indicators

def Strategy_dumb(ticker, list_data):
    """
    Simple strategy
    Args:
    - ticker: str | Stock ticker symbol, typically "AAPL" ...
    - list_data: list | List containing the last three prices
    """
    if len(list_data) < 3:
        raise ValueError("list_data must contain the last three prices.")
    if list_data[0] < list_data[1] and list_data[1] < list_data[2]:
        return "BUY"
    elif list_data[0] > list_data[1] and list_data[1] > list_data[2]:
        return "SELL"
    return "HOLD"