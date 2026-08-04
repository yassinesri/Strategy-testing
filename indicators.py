import pandas as pd

def SMA(prices, window):
    """
    Simple Moving Average (SMA)
    Args:
    - prices: pd.Series | List of closing prices.
    - window: int | The number of periods to calculate the average over.
    Returns:
    - sma_values: pd.Series | List of SMA values
    """
    if window <= 0:
        raise ValueError("Window size must be a positive integer.")
    sma = prices.rolling(window=window).mean()
    return sma

def EMA(prices, window):
    """
    Exponential Moving Average (EMA)
    Args:
    - prices: pd.Series | List of closing prices.
    - window: int | The number of periods to calculate the average over.
    Returns:
    - ema: pd.Series | List of EMA values
    """
    if window <= 0:
        raise ValueError("Window size must be a positive integer.")
    ema = prices.ewm(span=window, adjust=False).mean()
    return ema

def MACD(prices, fast_period=12, slow_period=26, signal_period=9):
    """
    Moving Average Convergence Divergence (MACD)
    Args:
    - prices: pd.Series | List of closing prices.
    - fast_period: int | The number of periods for the fast EMA.
    - slow_period: int | The number of periods for the slow EMA.
    - signal_period: int | The number of periods for the signal line EMA.
    Returns:
    - macd_line: pd.Series | MACD line values
    - signal_line: pd.Series | Signal line values
    """
    if fast_period <= 0 or slow_period <= 0 or signal_period <= 0:
        raise ValueError("All periods must be positive integers.")
    
    ema_fast = EMA(prices, window=fast_period)
    ema_slow = EMA(prices, window=slow_period)
    macd_line = ema_fast - ema_slow
    signal_line = EMA(macd_line, window=signal_period)
    
    return macd_line, signal_line

def RSI(prices, window=14):
    """
    Relative Strength Index (RSI)
    Args:
    - prices: pd.Series | List of closing prices.
    - window: int | The number of periods to calculate the RSI over.
    Returns:
    - rsi: pd.Series | RSI values
    """
    if window <= 0:
        raise ValueError("Window size must be a positive integer.")
    
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = EMA(gain, window=window)
    avg_loss = EMA(loss, window=window)

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi

def stochastic_oscillator(prices, k_window=14, d_window=3):
    """
    Stochastic Oscillator
    Args:
    - prices: pd.Series | List of closing prices.
    - k_window: int | The number of periods for %K calculation.
    - d_window: int | The number of periods for %D calculation (moving average of %K).
    Returns:
    - percent_k: pd.Series | %K values
    - percent_d: pd.Series | %D values
    """
    if k_window <= 0 or d_window <= 0:
        raise ValueError("Window sizes must be positive integers.")
    
    low_min = prices.rolling(window=k_window).min()
    high_max = prices.rolling(window=k_window).max()
    
    percent_k = 100 * ((prices - low_min) / (high_max - low_min))
    percent_d = percent_k.rolling(window=d_window).mean()
    
    return percent_k, percent_d

def std(prices, window):
    """
    Standard Deviation
    Args:
    - prices: pd.Series | List of closing prices.
    - window: int | The number of periods to calculate the standard deviation over.
    Returns:
    - std_dev: pd.Series | Standard deviation values
    """
    if window <= 0:
        raise ValueError("Window size must be a positive integer.")
    
    std_dev = prices.rolling(window=window).std()
    return std_dev

def ATR(prices_high, prices_low, prices_close, window=14):
    """
    Average True Range (ATR)
    Args:
    - prices_high: pd.Series | List of high prices.
    - prices_low: pd.Series | List of low prices.
    - prices_close: pd.Series | List of closing prices.
    - window: int | The number of periods to calculate the ATR over.
    Returns:
    - atr: pd.Series | ATR values
    """
    if window <= 0:
        raise ValueError("Window size must be a positive integer.")
    
    tr1 = prices_high - prices_low
    tr2 = (prices_high - prices_close.shift()).abs()
    tr3 = (prices_low - prices_close.shift()).abs()
    
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    
    atr = true_range.rolling(window=window).mean()
    
    return atr

def VWAP(prices_high, prices_low, prices_close, volumes, window):
    """
    Volume Weighted Average Price (VWAP)
    Args:
    - prices_high: pd.Series | List of high prices.
    - prices_low: pd.Series | List of low prices.
    - prices_close: pd.Series | List of closing prices.
    - volumes: pd.Series | List of trading volumes.
    - window: int | The number of periods to calculate the VWAP over.
    Returns:
    - vwap: pd.Series | VWAP values
    """
    if window <= 0:
        raise ValueError("Window size must be a positive integer.")

    prices = (prices_high + prices_low + prices_close) / 3
    vwap = (prices * volumes).rolling(window=window).sum() / volumes.rolling(window=window).sum()
    
    return vwap