from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.pyplot import close

def generate_pdf(fig_worth, fig_returns_strategy, fig_returns_benchmark, fig_vol, report_filename = "backtest_report.pdf"):
    """
    Generate a PDF report containing the plots and analytics of the backtest.
    Args:
        fig_worth: matplotlib figure | Worth history plot
        fig_returns_strategy: matplotlib figure | Strategy returns plot
        fig_returns_benchmark: matplotlib figure | Benchmark returns plot
        fig_vol: matplotlib figure | Volatility clustering plot
    """
    with PdfPages(report_filename) as pdf:
        pdf.savefig(fig_worth)
        pdf.savefig(fig_returns_strategy)
        pdf.savefig(fig_returns_benchmark)
        pdf.savefig(fig_vol)

    close(fig_worth)
    close(fig_returns_strategy)
    close(fig_returns_benchmark)
    close(fig_vol)