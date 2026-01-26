"""Market data collector using yfinance."""

from datetime import datetime, timedelta
from typing import Optional
import logging

import pandas as pd

from .base import AssetClass

logger = logging.getLogger(__name__)

# Representative symbols for each asset class
ASSET_SYMBOLS = {
    AssetClass.EQUITY: {
        "SPY": "S&P 500 ETF",
        "QQQ": "NASDAQ 100 ETF",
        "IWM": "Russell 2000 ETF",
        "DIA": "Dow Jones ETF",
    },
    AssetClass.CRYPTO: {
        "BTC-USD": "Bitcoin",
        "ETH-USD": "Ethereum",
        "SOL-USD": "Solana",
    },
    AssetClass.FOREX: {
        "EURUSD=X": "EUR/USD",
        "GBPUSD=X": "GBP/USD",
        "USDJPY=X": "USD/JPY",
        "DX-Y.NYB": "US Dollar Index",
    },
    AssetClass.COMMODITY: {
        "GLD": "Gold ETF",
        "SLV": "Silver ETF",
        "USO": "Oil ETF",
        "UNG": "Natural Gas ETF",
    },
}

# Volatility indices
VOLATILITY_SYMBOLS = {
    "^VIX": "CBOE Volatility Index",
    "^VXN": "NASDAQ Volatility Index",
}


class MarketDataCollector:
    """
    Collector for market price data using yfinance.
    
    Used for:
    - Regime validation (compare sentiment to price action)
    - VIX data for regime classification
    - Backtesting ground truth
    """
    
    def __init__(self):
        """Initialize market data collector."""
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._yf = None
    
    def _get_yfinance(self):
        """Lazily import yfinance."""
        if self._yf is None:
            import yfinance as yf
            self._yf = yf
        return self._yf
    
    def get_prices(
        self,
        symbols: list[str],
        start_date: datetime,
        end_date: datetime,
        interval: str = "1d",
    ) -> pd.DataFrame:
        """
        Get historical price data for symbols.
        
        Args:
            symbols: List of ticker symbols
            start_date: Start date
            end_date: End date
            interval: Data interval ('1d', '1h', '5m', etc.)
            
        Returns:
            DataFrame with OHLCV data
        """
        yf = self._get_yfinance()
        
        # Adjust end date to include full day
        end_adjusted = end_date + timedelta(days=1)
        
        data = yf.download(
            tickers=symbols,
            start=start_date.strftime("%Y-%m-%d"),
            end=end_adjusted.strftime("%Y-%m-%d"),
            interval=interval,
            group_by="ticker",
            auto_adjust=True,
            progress=False,
        )
        
        return data
    
    def get_asset_class_prices(
        self,
        asset_class: AssetClass,
        start_date: datetime,
        end_date: datetime,
        interval: str = "1d",
    ) -> pd.DataFrame:
        """
        Get price data for all symbols in an asset class.
        
        Args:
            asset_class: Asset class to get data for
            start_date: Start date
            end_date: End date
            interval: Data interval
            
        Returns:
            DataFrame with OHLCV data for all symbols
        """
        symbols = list(ASSET_SYMBOLS.get(asset_class, {}).keys())
        
        if not symbols:
            self.logger.warning(f"No symbols configured for {asset_class}")
            return pd.DataFrame()
        
        return self.get_prices(
            symbols=symbols,
            start_date=start_date,
            end_date=end_date,
            interval=interval,
        )
    
    def get_vix(
        self,
        start_date: datetime,
        end_date: datetime,
        interval: str = "1d",
    ) -> pd.DataFrame:
        """
        Get VIX (volatility index) data.
        
        Args:
            start_date: Start date
            end_date: End date
            interval: Data interval
            
        Returns:
            DataFrame with VIX data
        """
        return self.get_prices(
            symbols=["^VIX"],
            start_date=start_date,
            end_date=end_date,
            interval=interval,
        )
    
    def get_current_vix(self) -> Optional[float]:
        """
        Get current VIX level.
        
        Returns:
            Current VIX value or None if unavailable
        """
        try:
            yf = self._get_yfinance()
            ticker = yf.Ticker("^VIX")
            hist = ticker.history(period="1d")
            
            if not hist.empty:
                return float(hist["Close"].iloc[-1])
            return None
        except Exception as e:
            self.logger.error(f"Error getting current VIX: {e}")
            return None
    
    def calculate_returns(
        self,
        prices: pd.DataFrame,
        period: int = 1,
    ) -> pd.DataFrame:
        """
        Calculate returns from price data.
        
        Args:
            prices: DataFrame with Close prices
            period: Number of periods for return calculation
            
        Returns:
            DataFrame with returns
        """
        if "Close" in prices.columns:
            return prices["Close"].pct_change(period)
        else:
            # Multi-ticker format
            closes = prices.xs("Close", axis=1, level=1)
            return closes.pct_change(period)
    
    def calculate_volatility(
        self,
        prices: pd.DataFrame,
        window: int = 20,
    ) -> pd.DataFrame:
        """
        Calculate rolling volatility.
        
        Args:
            prices: DataFrame with Close prices
            window: Rolling window size
            
        Returns:
            DataFrame with annualized volatility
        """
        returns = self.calculate_returns(prices)
        volatility = returns.rolling(window=window).std() * (252 ** 0.5)  # Annualized
        return volatility
    
    def health_check(self) -> bool:
        """Check if yfinance is working."""
        try:
            yf = self._get_yfinance()
            ticker = yf.Ticker("SPY")
            info = ticker.info
            return "symbol" in info
        except Exception as e:
            self.logger.error(f"Market data health check failed: {e}")
            return False
