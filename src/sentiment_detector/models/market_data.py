"""Market Data models for multi-asset price data."""

from datetime import date
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import BigInteger, Date, Float, Index, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from sentiment_detector.models.base import Base, TimestampMixin


class MarketData(Base, TimestampMixin):
    """
    Multi-market OHLCV price data.
    
    Sources:
    - COVID World Indices dataset (46 global indices)
    - Yahoo Finance (historical SPY, VIX, etc.)
    - Custom data sources
    
    Used for:
    - Cross-market regime analysis
    - GARCH-MIDAS volatility modeling
    - Backtesting validation
    """

    __tablename__ = "market_data"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )
    
    # Symbol identification
    symbol: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
        comment="Ticker symbol: SPY, ^GSPC, ^DJI, ^VIX, etc.",
    )
    
    # Asset metadata
    asset_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="index",
        comment="Asset type: index, stock, etf, crypto, commodity, forex",
    )
    
    exchange: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        comment="Exchange: NYSE, NASDAQ, LSE, TYO, etc.",
    )
    
    region: Mapped[Optional[str]] = mapped_column(
        String(10),
        nullable=True,
        comment="Region: us, eu, uk, jp, cn, etc.",
    )
    
    # Temporal information
    date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        index=True,
        comment="Trading date",
    )
    
    # OHLCV data
    open: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Opening price",
    )
    high: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="High price",
    )
    low: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Low price",
    )
    close: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        comment="Closing price",
    )
    adj_close: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Adjusted closing price (for splits/dividends)",
    )
    volume: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        nullable=True,
        comment="Trading volume",
    )
    
    # Computed fields (for convenience)
    daily_return: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Daily return (close-to-close)",
    )
    volatility: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
        comment="Realized volatility (rolling window)",
    )
    
    # Data source tracking
    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="unknown",
        comment="Data source: covid_indices, yahoo, tiingo, etc.",
    )

    __table_args__ = (
        # Unique constraint: one observation per symbol/date
        UniqueConstraint(
            "symbol", "date",
            name="uq_market_data_symbol_date",
        ),
        # Composite indexes for common queries
        Index(
            "ix_market_data_symbol_date",
            "symbol", "date",
        ),
        Index(
            "ix_market_data_source",
            "source",
        ),
        Index(
            "ix_market_data_asset_type",
            "asset_type",
        ),
    )

    def __repr__(self) -> str:
        return (
            f"<MarketData(symbol={self.symbol!r}, date={self.date}, "
            f"close={self.close:.2f})>"
        )
    
    @property
    def intraday_range(self) -> Optional[float]:
        """Calculate intraday price range as percentage."""
        if self.high and self.low and self.low > 0:
            return (self.high - self.low) / self.low * 100
        return None
    
    @property
    def gap(self) -> Optional[float]:
        """Calculate overnight gap (requires previous close, not stored)."""
        # This would need to be computed in a query with LAG
        return None
