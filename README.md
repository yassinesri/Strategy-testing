# Quantitative Strategy Backtesting Engine

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)

A Python engine for backtesting trading strategies on historical market data and generating a consolidated PDF report.

The engine is designed for systematic-investment experiments in which a fixed amount is contributed monthly.

## Features

- YAML-based configuration
- Historical market data download through `yfinance`
- Monthly cash deposits into a simulated portfolio
- Pluggable trading strategies, including intraday strategies for 5-minute data
- Buy-and-hold benchmark for comparison
- Portfolio value and NAV tracking
- Portfolio value and NAV visualizations
- Return distribution and Gaussian-model visualizations
- K-nearest-neighbours volatility-clustering analysis
- Consolidated PDF report containing the generated analytics

## Engineering approach

- **Object-oriented strategy design:** every strategy implements the `BaseStrategy` abstract interface for deposits, trading decisions, and invested capital.
- **Separation of concerns:** configuration loading, market-data retrieval, portfolio accounting, simulation, analytics, and visualization are isolated in focused modules.
- **Strategy factory:** `load_strategy` maps configuration names to concrete strategy classes without coupling the application entry point to individual implementations.
- **Numerical analysis:** pandas and NumPy provide time-series operations and vectorized indicator calculations where appropriate; scikit-learn supports volatility-regime classification.
- **Reproducible experiments:** ticker, date range, interval, contribution amount, strategy, and analytics parameters are defined in `config.yaml`.

## Requirements

- Python 3.10 or newer
- Internet access when downloading Yahoo Finance data

The pinned Python dependencies are listed in [requirements.txt](requirements.txt).

## Installation

From the project root:

```bash
python -m venv .venv
```

Activate the virtual environment.

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

## Configuration

Edit [config.yaml](config.yaml) before running a backtest:

```yaml
simulation:
  ticker: "WPEA.PA"
  interval: "5m"
  start_date: "2026-07-29"
  end_date: "2026-09-19"

portfolio:
  monthly_investment: 200.0

strategies:
  user_strategy: "mean_reversion"

analytics:
  volatility_clustering:
    window: 21
    n_neighbours: 15
```

Supported values for `strategies.user_strategy` are:

- `buy_and_hold`
- `mean_reversion`
- `moving_average_crossover`
- `test_strategy`

Yahoo Finance restricts the amount of historical data available for intraday intervals such as `5m`. Adjust the date range to remain within the provider's availability window for the selected interval.

The ticker must use Yahoo Finance's symbol format. For example, `AAPL` represents Apple on the US market and `WPEA.PA` represents a Paris-listed instrument.

## Running the project

Run the application from the project root:

```bash
python main.py
```

The program will:

1. Load the settings from `config.yaml`.
2. Download closing-price and volume data.
3. Run the selected strategy.
4. Run a buy-and-hold benchmark with the same monthly investment.
5. Generate a consolidated `backtest_report.pdf` containing performance, return, and volatility plots.

The report is written to the project root. Existing plotting functions can also be reused independently by passing Matplotlib axes to them.

## Analytics & visualizations

The application generates a portfolio-vs-benchmark chart, return time series, return distributions with Gaussian reference models, and KNN-based volatility-clustering charts using realized volatility and relative volume. These visualizations are assembled into `backtest_report.pdf` by `src/data/results.py`.



## Available strategies

### Buy and hold

`buy_and_hold` invests the monthly contribution and attempts to use the available account balance to buy the asset.

### Moving-average crossover

`moving_average_crossover` compares a short-term and long-term moving average. It buys when the short average is above the long average and sells when it is below it.

Its current defaults are:

- Short window: `20`
- Long window: `50`

### Mean reversion

`mean_reversion` compares the current price with a rolling average. It buys when the price is sufficiently below the average and sells when it is sufficiently above it.

Its current defaults are:

- Window: `20`
- Threshold: `0.02` (2 percent)

### Intraday drop and rebound

`test_strategy` is designed for intraday data, such as the configured `5m` interval. At the start of each day it records the first observed price. If the price falls by `drop_threshold` from that reference, it sells the full position. While out of the position, it tracks the lowest observed price and buys the full position again when the price rebounds by `rise_threshold` from that low.

Its current defaults are:

- Drop threshold: `0.02` (2 percent)
- Rise threshold: `0.02` (2 percent)

## Project structure

```text
.
|-- config.yaml
|-- main.py
|-- requirements.txt
|-- src/
  |-- analytics/
  |   |-- indicators.py          # Metrics and statistical indicators
  |   `-- plotting.py            # Charts and printed statistics
  |-- core/
  |   |-- engine.py              # Backtest execution loop
  |   `-- portfolio.py           # Account and position management
  |-- data/
  |   |-- load_config.py         # YAML configuration loader
  |   |-- load_financial_data.py # Yahoo Finance data loader
  |   |-- results.py              # PDF report generation
  |   `-- load_strategy.py       # Strategy name-to-class loader
  `-- strategies/
      |-- base.py               # BaseStrategy abstract class
      |-- buy_and_hold.py
      |-- mean_reversion.py
      |-- moving_average_crossover.py
      `-- test_strategy.py       # Intraday drop-and-rebound strategy
```

## Adding a strategy

1. Create a module in `src/strategies/`.
2. Define a class inheriting from `BaseStrategy`.
3. Implement `__init__` (with any required arguments), `deposit`, `decision`, and `total_invested`.
4. Add the class to `STRATEGIES` in [load_strategy.py](src/data/load_strategy.py).
5. Add its string name to the supported values in `config.yaml`.

Example:

```python
from .base import BaseStrategy


class MyStrategy(BaseStrategy):
    def __init__(self, ticker, amount_to_invest_monthly):
        super().__init__(ticker)
        self.amount_to_invest_monthly = amount_to_invest_monthly

    def deposit(self, date):
        return self.amount_to_invest_monthly

    def decision(self, price):
        return "Hold", 0

    def total_invested(self):
        return 0
```

The backtest engine instantiates the selected class as follows:

```python
strategy_class = load_strategy("my_strategy")
simulate_a_strategy(strategy_class, prices_data, ticker, monthly_investment)
```

`simulate_a_strategy` returns two values: portfolio worth history and NAV history. The strategy class receives the ticker and monthly investment through the positional arguments passed to the engine.

## Notes

- This project is intended for research and experimentation, not financial advice.
- Backtests do not guarantee future performance.
- The current portfolio model does not include transaction fees, slippage, taxes, or order execution delays.
- Data availability depends on Yahoo Finance and the selected ticker, date range, and interval.
