import yfinance as yf


def import_data(ticker: str, column: str,interval: str, start_date: str, end_date: str):
    """
    Download historical price data for a ticker and return the specified prices as a list.
    Args:
    - ticker: str | Stock ticker symbol, typically "AAPL" ...
    - column: str | The column of the data to return, typically "Close" for closing prices.
    - interval: str | Data interval, typically "1d", "1wk", or "1mo".
    - start_date: str | Start date for the data window (for example "2024-01-01").
    - end_date: str | End date for the data window (for example "2024-12-31").
    """

    valid_intervals = {"1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk", "1mo", "3mo"}
    if interval not in valid_intervals:
        raise ValueError(f"Unsupported interval '{interval}'. Choose one of: {sorted(valid_intervals)}")

    try:
        data = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            interval=interval,
            progress=False,
            auto_adjust=False,
        )
    except Exception as exc:
        raise RuntimeError(f"Failed to download data for ticker '{ticker}': {exc}") from exc

    if data.empty:
        raise RuntimeError(
            f"No data returned for ticker '{ticker}' with interval '{interval}' from {start_date} to {end_date}."
        )

    prices_data = data[column].squeeze().dropna()
    if prices_data.empty:
        raise RuntimeError(
            f"No {column.lower()} prices available for ticker '{ticker}' with interval '{interval}' from {start_date} to {end_date}."
        )

    return prices_data
    