from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

import src.analytics.plotting as plotting


def generate_pdf_old(fig_worth, fig_returns_strategy, fig_returns_benchmark, fig_vol, report_filename = "backtest_report.pdf"):
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

def generate_pdf(portfolio_worth, portfolio_nav, benchmark_worth, prices_data, volume_data, ticker, vol_window, vol_neighbors, filename="backtest_report.pdf"):
    """
    Generate a PDF report containing the plots and analytics of the backtest.
    Args:
    - portfolio_worth: pd.Series | Portfolio worth over time
    - portfolio_nav: pd.Series | Portfolio net asset value over time
    - benchmark_worth: pd.Series | Benchmark worth over time
    - prices_data: pd.Series | Benchmark price data
    - volume_data: pd.Series | Benchmark volume data
    - ticker: str | Ticker symbol of the asset
    - vol_window: int | Window size for volatility clustering analysis
    - vol_neighbors: int | Number of neighbors for volatility clustering analysis
    - filename: str | Name of the output PDF file
    """
    
    fig = plt.figure(figsize=(20, 20))
    ax_main = fig.add_subplot(4, 1, 1)
    ax_ret1 = fig.add_subplot(4, 2, 3)
    ax_ret2 = fig.add_subplot(4, 2, 4)
    ax_retb1 = fig.add_subplot(4, 2, 5)
    ax_retb2 = fig.add_subplot(4, 2, 6)
    ax_vol1 = fig.add_subplot(4, 2, 7)
    ax_vol2 = fig.add_subplot(4, 2, 8)
    
    # 3. On passe les axes correspondants à tes fonctions
    # (Assure-toi d'avoir bien modifié ces fonctions dans analytics.py au préalable)
    plotting.plot(portfolio_worth, "Strategy", benchmark_worth, f"Benchmark : {ticker}", ax=ax_main, title="Worth history", xlabel="Date", ylabel="Worth ($)")
    plotting.returns_analysis(portfolio_nav, "Portfolio", ax1=ax_ret1, ax2=ax_ret2)
    plotting.returns_analysis(prices_data, f"Benchmark : {ticker}", ax1=ax_retb1, ax2=ax_retb2)
    plotting.vol_clustering_analysis(prices_data, volume_data, ax1=ax_vol1, ax2=ax_vol2, window=vol_window, n_neighbours=vol_neighbors)
    
    # 4. Ajustement de l'espacement pour éviter que les textes se chevauchent
    plt.tight_layout()
    
    # 5. Sauvegarde de la figure unique dans le PDF
    with PdfPages(filename) as pdf:
        pdf.savefig(fig)
        
    # Nettoyage de la RAM
    plt.close(fig)