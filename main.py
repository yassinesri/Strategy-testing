import data
import engine
import strategy
import analytics


def main():
    ticker = "AAPL"
    interval = "1d"
    start_date = "2024-01-01"
    end_date = "2024-12-31"

    try:
        # For now, the simulation works with only one ticker at a time

        # Load the price data first
        prices_data = data.import_data(ticker, "Close", interval, start_date, end_date)

        # Benchmark simulation :
        benchmark_history, _, _ = engine.Simulate_a_Strategy(strategy.buy_and_hold, prices_data, ticker, 200)

        # Portfolio simulation :
        worth_history, nav_history, total_invested = engine.Simulate_a_Strategy(strategy.moving_average_crossover, prices_data, ticker, 200)

        # Visualization of the results
        analytics.plot(worth_history, "Strategy", benchmark_history, f"Benchmark : {ticker}", title="Worth history", xlabel="Date", ylabel="Worth ($)")
        analytics.print_statistics(worth_history, nav_history, benchmark_history, total_invested)
        
    except Exception as e:
        print(f"Error: {e}")


main()