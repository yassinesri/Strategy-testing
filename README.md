# Quantitative Strategy Backtesting Engine

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code style](https://img.shields.io/badge/Code%20style-PEP%208-blue.svg)](https://peps.python.org/pep-0008/)
[![Tests](https://img.shields.io/badge/Tests-pytest-blue.svg)](https://pytest.org/)

A configuration-driven Python engine for researching and backtesting trading strategies on historical market data.

The engine downloads price and volume data from Yahoo Finance, simulates a monthly-investment portfolio, compares a selected strategy with a buy-and-hold benchmark, and produces performance, return-distribution, and volatility-regime analytics.

## Features

- Historical market data download through `yfinance`
- Monthly cash deposits into a simulated portfolio
- Pluggable trading strategies with a shared abstract interface
- Buy-and-hold benchmark for comparison
- Portfolio value and NAV tracking
- Performance statistics:
  - ROI
  - Maximum drawdown
  - Alpha and beta
  - Sharpe ratio
  - Sortino ratio
- Return distribution and Gaussian-model visualizations
- K-nearest-neighbours volatility-clustering analysis using price returns and volume
- YAML-based configuration

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
  interval: "1d"
  start_date: "2023-01-01"
  end_date: "2025-12-31"

portfolio:
  monthly_investment: 200.0

strategies:
  user_strategy: "moving_average_crossover"

analytics:
  volatility_clustering:
    window: 21
    n_neighbours: 15
```

Supported values for `strategies.user_strategy` are:

- `buy_and_hold`
- `mean_reversion`
- `moving_average_crossover`

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
5. Print portfolio statistics.
6. Display performance, return, and volatility plots.

The plotting functions open interactive Matplotlib windows, so the process may remain active until the figures are closed.

## Analytics & visualizations

The application generates portfolio-vs-benchmark charts, return time series, return distributions with a Gaussian reference model, and KNN-based volatility-clustering charts using realized volatility and relative volume.

![Backtest Analytics](docs/backtest_results.png)

> The image above is a placeholder for a representative backtest output. Add a generated figure at `docs/backtest_results.png` when publishing results.

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
  |   `-- load_strategy.py       # Strategy name-to-class loader
  `-- strategies/
      |-- base.py               # BaseStrategy abstract class
      |-- buy_and_hold.py
      |-- mean_reversion.py
      `-- moving_average_crossover.py
```

## Testing & quality assurance

Run the test suite from the project root:

```bash
python -m pytest
```

For static analysis, install the optional development tools and run:

```bash
python -m pip install pytest mypy ruff
python -m mypy src
python -m ruff check .
```

The repository currently provides the application and strategy modules; add tests under `tests/` as the strategy library grows. High-value tests should cover strategy decisions, monthly deposit behavior, invalid configuration names, portfolio accounting, and indicator edge cases.

## Adding a strategy

1. Create a module in `src/strategies/`.
2. Define a class inheriting from `BaseStrategy`.
3. Implement `deposit`, `decision`, and `total_invested`.
4. Add the class to `STRATEGIES` in [load_strategy.py](src/data/load_strategy.py).
5. Add its string name to the supported values in `config.yaml`.

Example:

```python
from .base import BaseStrategy


class MyStrategy(BaseStrategy):
    def deposit(self, date):
        return 0

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

## Notes

- This project is intended for research and experimentation, not financial advice.
- Backtests do not guarantee future performance.
- The current portfolio model does not include transaction fees, slippage, taxes, or order execution delays.
- Data availability depends on Yahoo Finance and the selected ticker, date range, and interval.
