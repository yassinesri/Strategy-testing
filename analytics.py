import matplotlib.pyplot as plt
import pandas as pd
import indicators


def plot(*args, title="Time Series Analysis", xlabel="Date", ylabel="Value", figsize=(12, 6), grid=True, legend=True):
    """
    Plot multiple pandas Series on the same figure.
    Args :
    - *args: Variable length argument list. Should be pairs of (series, label).
    - title: str | Title of the plot.
    - xlabel: str | Label for the x-axis.
    - ylabel: str | Label for the y-axis.
    - figsize: tuple | Size of the figure.
    - grid: bool | Whether to display a grid.
    - legend: bool | Whether to display a legend.
    """
    if len(args) % 2 != 0:
        raise ValueError("Expected an even number of arguments: series, label, series, label, ...")

    plt.figure(figsize=figsize)

    for i in range(0, len(args), 2):
        series = args[i]
        label = args[i + 1]

        if not isinstance(label, str):
            raise TypeError("Each label must be a string.")

        plt.plot(series, label=label)

    plt.title(title, fontsize=14)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if legend:
        plt.legend()
    if grid:
        plt.grid(True)

    plt.show()


def print_statistics(worth_portfolio, nav_history, benchmark_history, total_invested):
    """
    Print the main portfolio statistics.

    Args:
        worth_portfolio (pd.Series): Portfolio value history.
        benchmark_history (pd.Series): Benchmark value history.
        total_invested (float, optional): Total amount invested. Defaults to None.
    """
    if total_invested is None:
        total_invested = worth_portfolio.iloc[0]

    roi_portfolio, roi_score = indicators.ROI(total_invested, worth_portfolio.iloc[-1])
    roi_benchmark, _ = indicators.ROI(total_invested, benchmark_history.iloc[-1])
    max_drawdown, md_score = indicators.Max_Drawdown(worth_portfolio)
    beta_value, beta_score = indicators.beta(benchmark_history, worth_portfolio)
    alpha_value, alpha_score = indicators.alpha(benchmark_history, worth_portfolio, beta_value)
    sharpe, sharpe_score = indicators.sharpe_ratio(worth_portfolio)
    sortino, sortino_score = indicators.sortino_ratio(nav_history)

    print("Portfolio Statistics")
    print("-" * 28)
    print(f"ROI: {roi_portfolio:.2f}%  ({roi_score})")
    print(f"Max Drawdown: {max_drawdown:.2f}%  ({md_score})")
    print(f"Alpha: {alpha_value:.2f}  ({alpha_score})")
    print(f"Beta: {beta_value:.2f}  ({beta_score})")
    print(f"Sharpe Ratio: {sharpe:.2f}  ({sharpe_score})")
    print(f"Sortino Ratio: {sortino:.2f}  ({sortino_score})")


