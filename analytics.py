import matplotlib.pyplot as plt


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


def Cumulative_Return():
    pass

def Max_Drawdown():
    pass

def Sharpe_Ratio():
    pass

def MC_Simulation():
    pass