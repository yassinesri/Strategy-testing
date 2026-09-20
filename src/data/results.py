from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

import src.analytics.plotting as plotting


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
    plt.style.use('ggplot')
    fig = plt.figure(figsize=(20, 20))
    fig.suptitle(f"Backtest Report : Strategy vs {ticker}", fontsize=20, fontweight='bold')

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
    fig.tight_layout(rect=[0, 0, 1, 0.97], h_pad=2.0)
    
    # 5. Sauvegarde de la figure unique dans le PDF
    with PdfPages(filename) as pdf:
        pdf.savefig(fig)
        
    # Nettoyage de la RAM
    plt.close(fig)