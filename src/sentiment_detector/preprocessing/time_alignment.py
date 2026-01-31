"""
Time Alignment Algorithm for Mixed-Frequency Financial Data.

Implements the Forward-Fill with Aggregation algorithm from Dakalbab et al. (2025)
and the Next-Day Attribution logic from Kengmegni (2024).

This module handles the alignment of irregular sentiment events to fixed price intervals,
which is critical for GARCH-MIDAS and Jump Model inputs.
"""

from dataclasses import dataclass, field
from datetime import datetime, date, time, timedelta
from enum import Enum
from typing import Optional, Union, Iterator
import logging

import pandas as pd
import numpy as np

from .timezone_handler import TimezoneHandler, MarketTimezone, MARKET_CUTOFF_TIME

logger = logging.getLogger(__name__)


class AlignmentCase(str, Enum):
    """
    Alignment case classification following Dakalbab et al. (2025).
    """
    PERFECT_MATCH = "perfect_match"    # Case 1: News in [t-1, t] maps to p_t
    FORWARD_FILL = "forward_fill"       # Case 2: No news, use S_last
    AGGREGATED = "aggregated"           # Case 3: Multiple articles, use AIS_t


@dataclass
class AlignmentResult:
    """
    Result of aligning sentiment data to a price interval.
    
    Attributes:
        trading_date: The trading date this alignment corresponds to
        interval_start: Start of the interval
        interval_end: End of the interval
        case: Which alignment case was applied
        sentiment_score: The aligned sentiment score
        positive_score: Aggregated positive sentiment
        negative_score: Aggregated negative sentiment
        neutral_score: Aggregated neutral sentiment
        document_count: Number of documents in interval
        sources: List of sources contributing to this interval
        asset_class: The asset class this alignment is for
        last_sentiment_date: For forward-fill, when the carried sentiment originated
        metadata: Additional alignment metadata
    """
    trading_date: datetime
    interval_start: datetime
    interval_end: datetime
    case: AlignmentCase
    sentiment_score: float  # Net sentiment (P - N)
    positive_score: float
    negative_score: float
    neutral_score: float
    document_count: int
    sources: list[str] = field(default_factory=list)
    asset_class: Optional[str] = None
    last_sentiment_date: Optional[datetime] = None
    metadata: dict = field(default_factory=dict)
    
    @property
    def ais_label(self) -> str:
        """
        Get the Aggregated Interval Sentiment label.
        Following Dakalbab: AIS > 0 → Positive, AIS < 0 → Negative
        """
        if self.sentiment_score > 0:
            return "positive"
        elif self.sentiment_score < 0:
            return "negative"
        else:
            return "neutral"


class TimeAligner:
    """
    Aligns irregular sentiment events to fixed price intervals.
    
    Implements:
    1. Timestamp standardization with 4:30 PM EST cutoff (Kengmegni, 2024)
    2. Three-case alignment logic (Dakalbab et al., 2025):
       - Case 1: Perfect match (news in interval)
       - Case 2: Forward-fill (sparse data)
       - Case 3: Aggregation (high velocity)
    
    Example:
        >>> aligner = TimeAligner()
        >>> results = aligner.align_to_daily(sentiment_df, price_dates)
        >>> for result in results:
        ...     print(f"{result.trading_date}: {result.case} -> {result.sentiment_score}")
    """
    
    def __init__(
        self,
        target_timezone: MarketTimezone = MarketTimezone.EST,
        cutoff_time: time = MARKET_CUTOFF_TIME,
        max_forward_fill_days: int = 5
    ):
        """
        Initialize time aligner.
        
        Args:
            target_timezone: Target timezone for alignment
            cutoff_time: Daily cutoff for next-day attribution
            max_forward_fill_days: Maximum days to forward-fill before using neutral
        """
        self.timezone_handler = TimezoneHandler(
            target_timezone=target_timezone,
            cutoff_time=cutoff_time
        )
        self.max_forward_fill_days = max_forward_fill_days
        
    def align_to_daily(
        self,
        sentiment_data: pd.DataFrame,
        trading_dates: list[datetime],
        timestamp_col: str = "created_at",
        sentiment_col: str = "compound",
        positive_col: str = "positive",
        negative_col: str = "negative",
        neutral_col: str = "neutral",
        source_col: str = "source",
        asset_class_col: Optional[str] = "asset_class"
    ) -> list[AlignmentResult]:
        """
        Align sentiment data to daily price intervals.
        
        Args:
            sentiment_data: DataFrame with sentiment scores and timestamps
            trading_dates: List of trading dates to align to
            timestamp_col: Column containing timestamps
            sentiment_col: Column containing compound sentiment score
            positive_col: Column containing positive score
            negative_col: Column containing negative score
            neutral_col: Column containing neutral score
            source_col: Column containing data source
            asset_class_col: Column containing asset class (optional)
            
        Returns:
            List of AlignmentResult objects, one per trading date
        """
        if sentiment_data.empty:
            logger.warning("Empty sentiment data provided for alignment")
            return []
        
        # Normalize all timestamps and get trading dates
        sentiment_data = sentiment_data.copy()
        sentiment_data["_aligned_timestamp"] = sentiment_data[timestamp_col].apply(
            self.timezone_handler.normalize_timestamp
        )
        sentiment_data["_trading_date"] = sentiment_data["_aligned_timestamp"].apply(
            self.timezone_handler.get_trading_date
        )
        
        # Sort trading dates
        trading_dates = sorted(trading_dates)
        
        results = []
        last_sentiment: Optional[dict] = None
        last_sentiment_date: Optional[datetime] = None
        
        for i, trading_date in enumerate(trading_dates):
            # Get interval bounds
            interval_start, interval_end = self.timezone_handler.get_interval_bounds(
                trading_date, interval_type="daily"
            )
            
            # Filter sentiment data for this interval
            mask = sentiment_data["_trading_date"] == trading_date
            interval_data = sentiment_data[mask]
            
            document_count = len(interval_data)
            
            if document_count == 0:
                # Case 2: Forward-Fill
                result = self._handle_forward_fill(
                    trading_date=trading_date,
                    interval_start=interval_start,
                    interval_end=interval_end,
                    last_sentiment=last_sentiment,
                    last_sentiment_date=last_sentiment_date
                )
            elif document_count == 1:
                # Case 1: Perfect Match (single document)
                row = interval_data.iloc[0]
                result = AlignmentResult(
                    trading_date=trading_date,
                    interval_start=interval_start,
                    interval_end=interval_end,
                    case=AlignmentCase.PERFECT_MATCH,
                    sentiment_score=row.get(sentiment_col, 0.0),
                    positive_score=row.get(positive_col, 0.0),
                    negative_score=row.get(negative_col, 0.0),
                    neutral_score=row.get(neutral_col, 0.0),
                    document_count=1,
                    sources=[row.get(source_col, "unknown")],
                    asset_class=row.get(asset_class_col) if asset_class_col else None,
                )
                # Update last sentiment for forward-fill
                last_sentiment = {
                    "compound": row.get(sentiment_col, 0.0),
                    "positive": row.get(positive_col, 0.0),
                    "negative": row.get(negative_col, 0.0),
                    "neutral": row.get(neutral_col, 0.0),
                }
                last_sentiment_date = trading_date
                
            else:
                # Case 3: Aggregation (multiple documents)
                result = self._handle_aggregation(
                    interval_data=interval_data,
                    trading_date=trading_date,
                    interval_start=interval_start,
                    interval_end=interval_end,
                    sentiment_col=sentiment_col,
                    positive_col=positive_col,
                    negative_col=negative_col,
                    neutral_col=neutral_col,
                    source_col=source_col,
                    asset_class_col=asset_class_col
                )
                # Update last sentiment
                last_sentiment = {
                    "compound": result.sentiment_score,
                    "positive": result.positive_score,
                    "negative": result.negative_score,
                    "neutral": result.neutral_score,
                }
                last_sentiment_date = trading_date
            
            results.append(result)
        
        logger.info(
            f"Aligned {len(sentiment_data)} documents to {len(results)} intervals. "
            f"Cases: {self._count_cases(results)}"
        )
        
        return results
    
    def _handle_forward_fill(
        self,
        trading_date: datetime,
        interval_start: datetime,
        interval_end: datetime,
        last_sentiment: Optional[dict],
        last_sentiment_date: Optional[datetime]
    ) -> AlignmentResult:
        """
        Handle Case 2: Forward-fill when no data in interval.
        
        Per Dakalbab et al. (2025): Carry forward the last sentiment score
        to ensure continuous feature vector for the Jump Model.
        """
        if last_sentiment is None or last_sentiment_date is None:
            # No prior data - use neutral
            return AlignmentResult(
                trading_date=trading_date,
                interval_start=interval_start,
                interval_end=interval_end,
                case=AlignmentCase.FORWARD_FILL,
                sentiment_score=0.0,
                positive_score=0.0,
                negative_score=0.0,
                neutral_score=1.0,
                document_count=0,
                sources=[],
                metadata={"reason": "no_prior_data"}
            )
        
        # Check if forward-fill is too old
        days_since_last = (trading_date - last_sentiment_date).days
        if days_since_last > self.max_forward_fill_days:
            # Too stale - decay to neutral
            decay_factor = 0.5 ** (days_since_last - self.max_forward_fill_days)
            return AlignmentResult(
                trading_date=trading_date,
                interval_start=interval_start,
                interval_end=interval_end,
                case=AlignmentCase.FORWARD_FILL,
                sentiment_score=last_sentiment["compound"] * decay_factor,
                positive_score=last_sentiment["positive"] * decay_factor,
                negative_score=last_sentiment["negative"] * decay_factor,
                neutral_score=last_sentiment["neutral"] + (1 - decay_factor) * (1 - last_sentiment["neutral"]),
                document_count=0,
                sources=[],
                last_sentiment_date=last_sentiment_date,
                metadata={"decay_factor": decay_factor, "days_since_last": days_since_last}
            )
        
        return AlignmentResult(
            trading_date=trading_date,
            interval_start=interval_start,
            interval_end=interval_end,
            case=AlignmentCase.FORWARD_FILL,
            sentiment_score=last_sentiment["compound"],
            positive_score=last_sentiment["positive"],
            negative_score=last_sentiment["negative"],
            neutral_score=last_sentiment["neutral"],
            document_count=0,
            sources=[],
            last_sentiment_date=last_sentiment_date,
            metadata={"days_since_last": days_since_last}
        )
    
    def _handle_aggregation(
        self,
        interval_data: pd.DataFrame,
        trading_date: datetime,
        interval_start: datetime,
        interval_end: datetime,
        sentiment_col: str,
        positive_col: str,
        negative_col: str,
        neutral_col: str,
        source_col: str,
        asset_class_col: Optional[str]
    ) -> AlignmentResult:
        """
        Handle Case 3: Aggregate multiple documents in interval.
        
        Per Dakalbab et al. (2025):
        AIS_t = Σ Sentiment(e_i) for all articles in [t-1, t]
        """
        # Calculate Aggregated Interval Sentiment (AIS_t)
        # Using sum per Dakalbab's specification
        ais_t = interval_data[sentiment_col].sum()
        
        # Also calculate means for individual components
        positive_mean = interval_data[positive_col].mean() if positive_col in interval_data.columns else 0.0
        negative_mean = interval_data[negative_col].mean() if negative_col in interval_data.columns else 0.0
        neutral_mean = interval_data[neutral_col].mean() if neutral_col in interval_data.columns else 0.0
        
        # Get unique sources
        sources = interval_data[source_col].unique().tolist() if source_col in interval_data.columns else []
        
        # Get asset class (most common if multi-label supported)
        asset_class = None
        if asset_class_col and asset_class_col in interval_data.columns:
            asset_class = interval_data[asset_class_col].mode().iloc[0] if not interval_data[asset_class_col].mode().empty else None
        
        return AlignmentResult(
            trading_date=trading_date,
            interval_start=interval_start,
            interval_end=interval_end,
            case=AlignmentCase.AGGREGATED,
            sentiment_score=ais_t,
            positive_score=positive_mean,
            negative_score=negative_mean,
            neutral_score=neutral_mean,
            document_count=len(interval_data),
            sources=sources,
            asset_class=asset_class,
            metadata={
                "ais_sum": ais_t,
                "sentiment_std": interval_data[sentiment_col].std(),
                "sentiment_min": interval_data[sentiment_col].min(),
                "sentiment_max": interval_data[sentiment_col].max(),
            }
        )
    
    def _count_cases(self, results: list[AlignmentResult]) -> dict:
        """Count occurrences of each alignment case."""
        counts = {case: 0 for case in AlignmentCase}
        for result in results:
            counts[result.case] += 1
        return {k.value: v for k, v in counts.items()}
    
    def align_to_hourly(
        self,
        sentiment_data: pd.DataFrame,
        start_date: datetime,
        end_date: datetime,
        **kwargs
    ) -> list[AlignmentResult]:
        """
        Align sentiment data to hourly intervals.
        
        Useful for intraday analysis of crypto/forex markets.
        
        Args:
            sentiment_data: DataFrame with sentiment scores
            start_date: Start of period
            end_date: End of period
            **kwargs: Additional arguments passed to align_to_daily logic
            
        Returns:
            List of AlignmentResult objects, one per hour
        """
        # Generate hourly intervals
        current = start_date.replace(minute=0, second=0, microsecond=0)
        hourly_intervals = []
        while current <= end_date:
            hourly_intervals.append(current)
            current += timedelta(hours=1)
        
        # For now, delegate to daily logic with adapted interval bounds
        # Full hourly implementation would need interval_type parameter
        logger.warning("Hourly alignment currently uses adapted daily logic. Full hourly support coming in Phase 2.")
        return self.align_to_daily(sentiment_data, hourly_intervals, **kwargs)
    
    def align_dataframe(
        self,
        sentiment_data: pd.DataFrame,
        trading_dates: list[datetime],
        **kwargs
    ) -> pd.DataFrame:
        """
        Align sentiment data and return as DataFrame.
        
        Convenience method for downstream pandas/sklearn workflows.
        
        Args:
            sentiment_data: Input sentiment DataFrame
            trading_dates: Trading dates to align to
            **kwargs: Arguments passed to align_to_daily
            
        Returns:
            DataFrame with aligned sentiment features
        """
        results = self.align_to_daily(sentiment_data, trading_dates, **kwargs)
        
        records = []
        for r in results:
            records.append({
                "trading_date": r.trading_date,
                "alignment_case": r.case.value,
                "sentiment": r.sentiment_score,
                "positive": r.positive_score,
                "negative": r.negative_score,
                "neutral": r.neutral_score,
                "document_count": r.document_count,
                "ais_label": r.ais_label,
                "asset_class": r.asset_class,
                **{f"meta_{k}": v for k, v in r.metadata.items() if isinstance(v, (int, float, str, bool))}
            })
        
        return pd.DataFrame(records)


def create_trading_date_range(
    start_date: Union[datetime, date, str],
    end_date: Union[datetime, date, str],
    exclude_weekends: bool = True
) -> list[datetime]:
    """
    Create a list of trading dates between start and end.
    
    Args:
        start_date: Start date
        end_date: End date
        exclude_weekends: Whether to exclude Saturday/Sunday
        
    Returns:
        List of trading dates as datetime objects
    """
    from zoneinfo import ZoneInfo
    
    est_tz = ZoneInfo("America/New_York")
    
    # Parse dates
    if isinstance(start_date, str):
        start_date = datetime.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = datetime.fromisoformat(end_date)
    
    if hasattr(start_date, 'date'):
        start_date = start_date.date() if isinstance(start_date, datetime) else start_date
    if hasattr(end_date, 'date'):
        end_date = end_date.date() if isinstance(end_date, datetime) else end_date
    
    dates = []
    current = start_date
    while current <= end_date:
        if not exclude_weekends or current.weekday() < 5:
            dt = datetime.combine(current, time.min, tzinfo=est_tz)
            dates.append(dt)
        current += timedelta(days=1)
    
    return dates
