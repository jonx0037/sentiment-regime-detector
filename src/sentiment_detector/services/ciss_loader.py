"""
CISS Data Loader for GARCH-MIDAS Integration.

Loads ECB CISS (Composite Indicator of Systemic Stress) data
and prepares it for use as an exogenous variable in the 
GARCH-MIDAS volatility model.

ECB CISS Features:
- Daily frequency (since 1999, weekly before)
- Values range 0-1, with higher = more stress
- Captures cross-correlations between 5 market segments:
  1. Money market
  2. Bond market
  3. Equity market
  4. Foreign exchange
  5. Financial intermediaries

Usage:
    loader = CISSDataLoader()
    ciss_series = await loader.load_ciss_series(start_date, end_date)
    result = garch_midas.fit(returns, sentiment=ciss_series)
"""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, Tuple, List, Dict
import logging

import numpy as np
import pandas as pd

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

logger = logging.getLogger(__name__)


@dataclass
class CISSData:
    """Container for CISS data with metadata."""
    
    series: pd.Series  # Daily CISS values indexed by date
    source: str  # Data source (ecb_ciss)
    region: str  # Geographic region (ea = Euro Area)
    date_range: Tuple[date, date]  # Start and end dates
    n_observations: int
    
    # Summary statistics
    mean: float
    std: float
    min: float
    max: float
    
    # Crisis detection thresholds
    high_stress_threshold: float = 0.35
    crisis_threshold: float = 0.50
    
    # Crisis periods detected
    high_stress_periods: List[Tuple[date, date]] = None
    crisis_periods: List[Tuple[date, date]] = None
    
    def __post_init__(self):
        """Detect crisis periods after initialization."""
        if self.high_stress_periods is None:
            self.high_stress_periods = self._detect_periods(self.high_stress_threshold)
        if self.crisis_periods is None:
            self.crisis_periods = self._detect_periods(self.crisis_threshold)
    
    def _detect_periods(self, threshold: float) -> List[Tuple[date, date]]:
        """Detect contiguous periods above threshold."""
        above = self.series >= threshold
        periods = []
        
        start = None
        for dt, is_above in above.items():
            if is_above and start is None:
                start = dt
            elif not is_above and start is not None:
                periods.append((start, dt))
                start = None
        
        if start is not None:
            periods.append((start, above.index[-1]))
        
        return periods
    
    def get_regime_labels(self) -> pd.Series:
        """
        Convert CISS values to regime labels.
        
        Returns:
            Series with labels: 'calm', 'elevated', 'high_stress', 'crisis'
        """
        labels = pd.Series(index=self.series.index, dtype=str)
        labels[self.series < 0.15] = 'calm'
        labels[(self.series >= 0.15) & (self.series < 0.35)] = 'elevated'
        labels[(self.series >= 0.35) & (self.series < 0.50)] = 'high_stress'
        labels[self.series >= 0.50] = 'crisis'
        return labels
    
    def summary(self) -> str:
        """Generate summary report."""
        lines = [
            "ECB CISS Data Summary",
            "=" * 40,
            f"Region: {self.region}",
            f"Date Range: {self.date_range[0]} to {self.date_range[1]}",
            f"Observations: {self.n_observations:,}",
            "",
            "Statistics:",
            f"  Mean: {self.mean:.4f}",
            f"  Std:  {self.std:.4f}",
            f"  Min:  {self.min:.4f}",
            f"  Max:  {self.max:.4f}",
            "",
            f"High Stress Periods (>= {self.high_stress_threshold}): {len(self.high_stress_periods)}",
            f"Crisis Periods (>= {self.crisis_threshold}): {len(self.crisis_periods)}",
        ]
        
        if self.crisis_periods:
            lines.append("\nMajor Crisis Periods:")
            for start, end in self.crisis_periods[:5]:  # Top 5
                peak = self.series.loc[start:end].max()
                lines.append(f"  {start} to {end} (peak: {peak:.4f})")
        
        return "\n".join(lines)


class CISSDataLoader:
    """
    Async data loader for ECB CISS stress indices.
    
    Provides methods to:
    - Load raw CISS series from database
    - Prepare for GARCH-MIDAS integration
    - Detect crisis periods
    - Generate ground truth regimes
    """
    
    def __init__(
        self,
        source: str = "ecb_ciss",
        region: str = "ea",  # Euro Area
    ):
        """
        Initialize loader.
        
        Args:
            source: Data source in stress_indices table
            region: Geographic region (ea, de, fr, etc.)
        """
        self.source = source
        self.region = region
    
    async def load_ciss_series(
        self,
        session: AsyncSession,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> CISSData:
        """
        Load CISS data as a pandas Series.
        
        Args:
            session: Async database session
            start_date: Start date (inclusive), None for all data
            end_date: End date (inclusive), None for all data
            
        Returns:
            CISSData object with series and metadata
        """
        # Build query
        query = """
            SELECT date, value, money_market, bond_market, equity_market, 
                   foreign_exchange, financial_intermediaries
            FROM stress_indices
            WHERE source = :source AND region = :region
        """
        params = {"source": self.source, "region": self.region}
        
        if start_date:
            query += " AND date >= :start_date"
            params["start_date"] = start_date
        
        if end_date:
            query += " AND date <= :end_date"
            params["end_date"] = end_date
        
        query += " ORDER BY date"
        
        result = await session.execute(text(query), params)
        rows = result.fetchall()
        await session.commit()
        
        if not rows:
            raise ValueError(f"No CISS data found for {self.source}/{self.region}")
        
        # Convert to DataFrame
        df = pd.DataFrame(rows, columns=[
            'date', 'value', 'money_market', 'bond_market', 'equity_market',
            'foreign_exchange', 'financial_intermediaries'
        ])
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        
        # Create series
        series = df['value'].astype(float)
        
        logger.info(f"Loaded {len(series)} CISS observations from {series.index.min().date()} to {series.index.max().date()}")
        
        return CISSData(
            series=series,
            source=self.source,
            region=self.region,
            date_range=(series.index.min().date(), series.index.max().date()),
            n_observations=len(series),
            mean=float(series.mean()),
            std=float(series.std()),
            min=float(series.min()),
            max=float(series.max()),
        )
    
    async def load_with_components(
        self,
        session: AsyncSession,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> pd.DataFrame:
        """
        Load CISS with all sub-components.
        
        Returns DataFrame with columns:
        - value: Overall CISS
        - money_market, bond_market, equity_market, 
          foreign_exchange, financial_intermediaries
        """
        ciss_data = await self.load_ciss_series(session, start_date, end_date)
        
        # Re-load with components
        query = """
            SELECT date, value, money_market, bond_market, equity_market, 
                   foreign_exchange, financial_intermediaries
            FROM stress_indices
            WHERE source = :source AND region = :region
        """
        params = {"source": self.source, "region": self.region}
        
        if start_date:
            query += " AND date >= :start_date"
            params["start_date"] = start_date
        if end_date:
            query += " AND date <= :end_date"
            params["end_date"] = end_date
        
        query += " ORDER BY date"
        
        result = await session.execute(text(query), params)
        rows = result.fetchall()
        await session.commit()
        
        df = pd.DataFrame(rows, columns=[
            'date', 'value', 'money_market', 'bond_market', 'equity_market',
            'foreign_exchange', 'financial_intermediaries'
        ])
        df['date'] = pd.to_datetime(df['date'])
        df = df.set_index('date')
        
        return df
    
    async def get_crisis_periods(
        self,
        session: AsyncSession,
        threshold: float = 0.35,
    ) -> List[Dict]:
        """
        Identify contiguous crisis periods.
        
        Args:
            session: Database session
            threshold: CISS value threshold for crisis
            
        Returns:
            List of crisis period dictionaries with:
            - start, end: dates
            - peak_value, peak_date
            - duration_days
            - name: crisis name if known
        """
        ciss = await self.load_ciss_series(session)
        
        # Known major crises for labeling
        KNOWN_CRISES = {
            (date(2008, 9, 1), date(2009, 6, 30)): "2008 Financial Crisis",
            (date(2010, 4, 1), date(2012, 12, 31)): "European Debt Crisis",
            (date(2020, 2, 1), date(2020, 6, 30)): "COVID-19 Crash",
            (date(2022, 1, 1), date(2022, 12, 31)): "2022 Market Stress",
        }
        
        periods = []
        above = ciss.series >= threshold
        
        start = None
        for dt, is_above in above.items():
            if is_above and start is None:
                start = dt
            elif not is_above and start is not None:
                end = dt
                period_data = ciss.series.loc[start:end]
                peak_idx = period_data.idxmax()
                
                # Check if matches known crisis
                crisis_name = None
                for (k_start, k_end), name in KNOWN_CRISES.items():
                    if k_start <= start.date() <= k_end or k_start <= end.date() <= k_end:
                        crisis_name = name
                        break
                
                periods.append({
                    'start': start.date(),
                    'end': end.date(),
                    'peak_value': float(period_data.max()),
                    'peak_date': peak_idx.date(),
                    'duration_days': (end - start).days,
                    'name': crisis_name,
                })
                start = None
        
        # Handle ongoing crisis
        if start is not None:
            end = ciss.series.index[-1]
            period_data = ciss.series.loc[start:end]
            peak_idx = period_data.idxmax()
            
            periods.append({
                'start': start.date(),
                'end': end.date(),
                'peak_value': float(period_data.max()),
                'peak_date': peak_idx.date(),
                'duration_days': (end - start).days,
                'name': None,
            })
        
        return periods


def prepare_ciss_for_garch_midas(
    ciss_series: pd.Series,
    returns_index: pd.DatetimeIndex,
    transformation: str = "raw",
) -> pd.Series:
    """
    Prepare CISS series for use in GARCH-MIDAS model.
    
    Args:
        ciss_series: Raw CISS values
        returns_index: DatetimeIndex from returns series
        transformation: How to transform CISS:
            - "raw": Use raw values (0-1)
            - "log": Log transform (log(ciss + 0.001))
            - "zscore": Z-score normalization
            - "rank": Rank transform to [0,1]
            
    Returns:
        Transformed CISS aligned to returns index
    """
    # Align to returns index (forward fill for missing days)
    aligned = ciss_series.reindex(returns_index, method='ffill')
    
    # Apply transformation
    if transformation == "raw":
        result = aligned
    elif transformation == "log":
        result = np.log(aligned + 0.001)
    elif transformation == "zscore":
        result = (aligned - aligned.mean()) / aligned.std()
    elif transformation == "rank":
        result = aligned.rank(pct=True)
    else:
        raise ValueError(f"Unknown transformation: {transformation}")
    
    # Handle any NaN at the start
    result = result.fillna(method='bfill').fillna(aligned.mean())
    
    return result


def combine_ciss_sentiment(
    ciss_series: pd.Series,
    sentiment_series: pd.Series,
    ciss_weight: float = 0.5,
) -> pd.Series:
    """
    Combine CISS and sentiment into a single index for GARCH-MIDAS.
    
    The combined index captures both:
    - Systemic stress (CISS) - market-wide risk
    - Sentiment - social/news-driven risk perception
    
    Args:
        ciss_series: CISS values (0-1, higher = more stress)
        sentiment_series: Sentiment values (-1 to 1, negative = bearish)
        ciss_weight: Weight for CISS (1-weight for sentiment)
        
    Returns:
        Combined index
    """
    # Normalize sentiment to 0-1 scale (inverted so negative = high risk)
    # Transform: -1 → 1 (high risk), +1 → 0 (low risk)
    sentiment_risk = (1 - sentiment_series) / 2
    
    # Align indices
    common_idx = ciss_series.index.intersection(sentiment_series.index)
    ciss_aligned = ciss_series.loc[common_idx]
    sentiment_aligned = sentiment_risk.loc[common_idx]
    
    # Weighted combination
    combined = ciss_weight * ciss_aligned + (1 - ciss_weight) * sentiment_aligned
    
    return combined
