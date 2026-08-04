import data
import engine
import strategy
import analytics


def main():
    tickers_list = ["AAPL"]
    interval = "1d"
    start_date = "2024-01-01"
    end_date = "2024-12-31"

    try:
        data.import_data(tickers_list[0], "Close", interval, start_date, end_date)
        engine.Simulate_a_Strategy(strategy.Strategy_dumb, data.prices_data)
        analytics.Cumulative_Returns()
        
    except Exception as e:
        print(f"Error: {e}")

main()