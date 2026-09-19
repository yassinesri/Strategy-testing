import logging

from src.data.load_config import load_config
from src.data.load_strategy import load_strategy
from src.data.load_financial_data import import_data
from src.core.engine import simulate_a_strategy
import src.analytics.plotting as plotting

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    # 1. Loading configuration
    try:
        logger.info("Loading configuration...")
        config = load_config("config.yaml")
    except Exception as e:
        logger.error(f"Fatal error during initialization : {e}")
        return

    # Extracting parameters
    ticker = config['simulation']['ticker']
    start_date = config['simulation']['start_date']
    end_date = config['simulation']['end_date']
    interval = config['simulation']['interval']
    capital = config['portfolio']['monthly_investment']

    logger.info(f"Starting backtest for {ticker} ({start_date} -> {end_date}).")

    try:
        # 2. Retrieving data
        prices_data = import_data(ticker, "Close", interval, start_date, end_date)
        volume_data = import_data(ticker, "Volume", interval, start_date, end_date)

        # 3. Simulation (Benchmark)
        BuyAndHoldStrategy = load_strategy("buy_and_hold")
        benchmark_worth, _, _ = simulate_a_strategy(
            BuyAndHoldStrategy, prices_data, ticker, capital)
        
        # 4. Simulation (Users's strategy)
        user_strategy = load_strategy(config['strategies']['user_strategy'])
        
        portfolio_worth, portfolio_nav, total_invested = simulate_a_strategy(
            user_strategy, prices_data, ticker, capital)

        # 5. Vizualization the results
        logger.info("Generating visualizations and analytics...")
        vol_window = config['analytics']['volatility_clustering']['window']
        vol_neighbors = config['analytics']['volatility_clustering']['n_neighbours']

        plotting.plot(portfolio_worth, "Strategy", benchmark_worth, f"Benchmark : {ticker}", title="Worth history", xlabel="Date", ylabel="Worth ($)")
        plotting.print_statistics(portfolio_worth, portfolio_nav, benchmark_worth, total_invested)
        plotting.returns_analysis(portfolio_nav, "Portfolio")
        plotting.returns_analysis(prices_data, f"Benchmark : {ticker}")
        plotting.vol_clustering_analysis(prices_data, volume_data, vol_window, vol_neighbors)
        
        logger.info("Backtest completed successfully.")

    except Exception as e:
        logger.error(f"An error occurred during the simulation : {e}")

if __name__ == "__main__":
    main()