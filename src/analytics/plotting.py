import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import src.analytics.indicators as indicators


def plot(*args, ax = None, title="Time Series Analysis", xlabel="Date", ylabel="Value", figsize=(12, 6), grid=True, legend=True):
    """
    Plot multiple pandas Series on the same figure.
    Args :
    - *args: Variable length argument list. Should be pairs of (series, label).
    - ax : matplotlib.axes.Axes | The axes on which to plot. If None, a new figure and axes are created.
    - title: str | Title of the plot.
    - xlabel: str | Label for the x-axis.
    - ylabel: str | Label for the y-axis.
    - figsize: tuple | Size of the figure.
    - grid: bool | Whether to display a grid.
    - legend: bool | Whether to display a legend.
    """
    if len(args) % 2 != 0:
        raise ValueError("Expected an even number of arguments: series, label, series, label, ...")

    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)

    for i in range(0, len(args), 2):
        series = args[i]
        label = args[i + 1]

        if not isinstance(label, str):
            raise TypeError("Each label must be a string.")

        ax.plot(series, label=label)

    ax.set_title(title, fontsize=14)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    if legend:
        ax.legend()
    if grid:
        ax.grid(True)



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

    roi_portfolio, roi_score = indicators.roi(total_invested, worth_portfolio.iloc[-1])
    max_drawdown, md_score = indicators.max_drawdown(worth_portfolio)
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


def returns_analysis(price_history, ch, ax1 = None, ax2 = None):
    """
    Show multiple plots to analyze the returns of a price_history pd.Series
    Args :
    - price_history : pd.Series or sequence of numeric price values (floats)
    - ch : string | Used to label the price history
    - ax1 : matplotlib.axes.Axes | The axes on which to plot the returns over time. If None, a new axes is created.
    - ax2 : matplotlib.axes.Axes | The axes on which to plot the returns distribution. If None, a new axes is created.
    """
    returns = indicators.returns(price_history).dropna()
    pdf_series, gauss_label = indicators.get_gaussian_model(returns)
    
    if ax1 is None or ax2 is None:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    ax1.stem(returns.index, returns.values, linefmt='grey', markerfmt='ro', basefmt='k-')
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Returns (%)")
    ax1.set_title(f"Returns over time (%) - {ch}")
    ax1.grid(True, linestyle='--', alpha=0.5)

    counts, bins, patches = ax2.hist(
        returns, 
        bins=50, 
        color='red', 
        edgecolor='white', 
        alpha=0.7,
        label="Empirical Data"
    )
    bin_width = bins[1] - bins[0]
    y_scaled = pdf_series * len(returns) * bin_width
    ax2.plot(pdf_series.index, y_scaled, color='black', linewidth=2.5, linestyle='-', label=gauss_label)

    ax2.set_xlabel("Returns (%)")
    ax2.set_ylabel("Number")
    ax2.set_title(f"Returns distribution - {ch}")
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.legend()


def vol_clustering_analysis(price_history, volume, ax1=None, ax2=None, window=21, n_neighbours=11):
    """
    Plots the regimes detected by the k-NN classification
    Args : 
    - price_history: pd.Series | List of daily prices
    - volume: pd.Series | List of daily volumes
    - ax1: matplotlib.axes.Axes | The axes on which to plot the volatility clustering. If None, a new axes is created.
    - ax2: matplotlib.axes.Axes | The axes on which to plot the 2D feature space. If None, a new axes is created.
    - window: int | Time window
    - n_neighbours: int | Number of neighbours
    """
    returns = indicators.returns(price_history).dropna()

    _, _, df = indicators.KNN_volatility_clustering(returns, volume, window, n_neighbours)

    color_map = {0: 'limegreen', 1: 'gold', 2: 'crimson'}
    df['Color'] = df['Predicted_Regime'].map(color_map)
    if ax1 is None or ax2 is None:
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    #1st graph : 
    ax1.plot(df.index, df['realized_vol'], color='black', alpha=0.2, linewidth=1)
    ax1.scatter(df.index, df['realized_vol'], c=df['Color'], s=15, zorder=3)
    ax1.axhspan(0, 15, color='limegreen', alpha=0.1)
    ax1.axhspan(15, 30, color='gold', alpha=0.1)
    max_vol = df['realized_vol'].max() + 5 
    ax1.axhspan(30, max_vol, color='crimson', alpha=0.1)
    ax1.set_title("KNN CLASSIFICATION OF VOLATILITY CLUSTERING REGIMES", fontweight='bold')
    ax1.set_ylabel(f"{window}-Day Realized Volatility (%)")
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.set_ylim(0, max_vol)

    # 2nd graph : 
    ax2.scatter(df['rolling_variance'], df['relative_volume_spike'], c=df['Color'], s=25, alpha=0.8, edgecolors='black', linewidth=0.5)
    ax2.set_title(f"2D FEATURE SPACE CLUSTERING (KNN, K={n_neighbours})", fontweight='bold')
    ax2.set_xlabel("Rolling Return Variance (X-Axis)")
    ax2.set_ylabel("Relative Volume Spike (Y-Axis)")
    ax2.grid(True, linestyle='--', alpha=0.5)
    green_patch = mpatches.Patch(color='limegreen', label='GREEN (0-15%)')
    yellow_patch = mpatches.Patch(color='gold', label='Medium Volatility (15-30%)')
    red_patch = mpatches.Patch(color='crimson', label='High (30%+)')
    ax1.legend(handles=[green_patch, yellow_patch, red_patch], loc='upper left')