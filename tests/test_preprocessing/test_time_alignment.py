"""
Unit tests for the time alignment module.

Tests the Dakalbab et al. (2024) time-alignment algorithm implementation.
"""

import pytest
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

import pandas as pd
import numpy as np

from src.sentiment_detector.preprocessing.time_alignment import (
    TimeAligner,
    AlignmentResult,
    AlignmentCase,
    create_trading_date_range,
)
from src.sentiment_detector.preprocessing.timezone_handler import (
    TimezoneHandler,
    MarketTimezone,
    MARKET_CUTOFF_TIME,
    normalize_source_timestamp,
)


class TestTimezoneHandler:
    """Tests for TimezoneHandler class."""
    
    def test_normalize_utc_timestamp(self):
        """Test normalizing UTC timestamp to EST."""
        handler = TimezoneHandler()
        
        # UTC timestamp
        utc_dt = datetime(2025, 1, 15, 18, 30, 0, tzinfo=ZoneInfo("UTC"))
        normalized = handler.normalize_timestamp(utc_dt)
        
        # Should be 1:30 PM EST (EST is UTC-5 in winter)
        assert normalized.tzinfo is not None
        assert normalized.hour == 13  # 18:30 UTC = 13:30 EST
    
    def test_normalize_unix_timestamp(self):
        """Test normalizing Unix epoch timestamp."""
        handler = TimezoneHandler()
        
        # Unix timestamp (seconds)
        unix_ts = 1705347600  # 2024-01-15 18:00:00 UTC
        normalized = handler.normalize_timestamp(unix_ts)
        
        assert isinstance(normalized, datetime)
        assert normalized.tzinfo is not None
    
    def test_normalize_iso_string(self):
        """Test normalizing ISO format string."""
        handler = TimezoneHandler()
        
        iso_str = "2025-01-15T18:30:00Z"
        normalized = handler.normalize_timestamp(iso_str)
        
        assert isinstance(normalized, datetime)
        assert normalized.hour == 13  # EST
    
    def test_trading_date_before_cutoff(self):
        """Test that timestamps before 4:30 PM map to same day."""
        handler = TimezoneHandler()
        
        # 2:00 PM EST - should be same day
        dt = datetime(2025, 1, 15, 14, 0, 0, tzinfo=ZoneInfo("America/New_York"))
        trading_date = handler.get_trading_date(dt)
        
        assert trading_date.date() == dt.date()
    
    def test_trading_date_after_cutoff(self):
        """Test that timestamps after 4:30 PM map to next day (Kengmegni, 2024)."""
        handler = TimezoneHandler()
        
        # 5:00 PM EST - should be next day
        dt = datetime(2025, 1, 15, 17, 0, 0, tzinfo=ZoneInfo("America/New_York"))
        trading_date = handler.get_trading_date(dt)
        
        assert trading_date.date() == dt.date() + timedelta(days=1)
    
    def test_weekend_adjustment(self):
        """Test that weekend dates are moved to Monday."""
        handler = TimezoneHandler()
        
        # Saturday after market close -> Monday
        saturday = datetime(2025, 1, 18, 17, 0, 0, tzinfo=ZoneInfo("America/New_York"))
        trading_date = handler.get_trading_date(saturday)
        
        assert trading_date.weekday() == 0  # Monday
    
    def test_market_hours_check(self):
        """Test market hours detection."""
        handler = TimezoneHandler()
        
        # During market hours
        market_time = datetime(2025, 1, 15, 11, 0, 0, tzinfo=ZoneInfo("America/New_York"))
        assert handler.is_market_hours(market_time) is True
        
        # After hours
        after_hours = datetime(2025, 1, 15, 18, 0, 0, tzinfo=ZoneInfo("America/New_York"))
        assert handler.is_market_hours(after_hours) is False
        
        # Weekend
        saturday = datetime(2025, 1, 18, 11, 0, 0, tzinfo=ZoneInfo("America/New_York"))
        assert handler.is_market_hours(saturday) is False


class TestTimeAligner:
    """Tests for TimeAligner class."""
    
    @pytest.fixture
    def sample_sentiment_data(self):
        """Create sample sentiment data for testing."""
        est_tz = ZoneInfo("America/New_York")
        
        data = pd.DataFrame({
            "created_at": [
                datetime(2025, 1, 13, 10, 0, 0, tzinfo=est_tz),  # Monday 10 AM
                datetime(2025, 1, 13, 14, 0, 0, tzinfo=est_tz),  # Monday 2 PM
                datetime(2025, 1, 13, 15, 0, 0, tzinfo=est_tz),  # Monday 3 PM
                datetime(2025, 1, 14, 11, 0, 0, tzinfo=est_tz),  # Tuesday 11 AM
                # Skip Wednesday - sparse data test
                datetime(2025, 1, 16, 9, 30, 0, tzinfo=est_tz),  # Thursday 9:30 AM
            ],
            "compound": [0.5, 0.3, -0.2, 0.8, -0.5],
            "positive": [0.6, 0.4, 0.1, 0.9, 0.0],
            "negative": [0.1, 0.1, 0.3, 0.1, 0.5],
            "neutral": [0.3, 0.5, 0.6, 0.0, 0.5],
            "source": ["twitter", "reddit", "twitter", "news", "twitter"],
            "asset_class": ["equity", "equity", "crypto", "equity", "crypto"],
        })
        return data
    
    @pytest.fixture
    def trading_dates(self):
        """Create trading dates for a week."""
        return create_trading_date_range("2025-01-13", "2025-01-17")
    
    def test_case1_perfect_match(self, sample_sentiment_data, trading_dates):
        """Test Case 1: Single document maps perfectly to interval."""
        aligner = TimeAligner()
        results = aligner.align_to_daily(sample_sentiment_data, trading_dates)
        
        # Tuesday should have single document -> perfect match
        tuesday_result = [r for r in results if r.trading_date.date().isoweekday() == 2][0]
        
        assert tuesday_result.case == AlignmentCase.PERFECT_MATCH
        assert tuesday_result.document_count == 1
        assert tuesday_result.sentiment_score == 0.8
    
    def test_case2_forward_fill(self, sample_sentiment_data, trading_dates):
        """Test Case 2: No data in interval -> forward fill."""
        aligner = TimeAligner()
        results = aligner.align_to_daily(sample_sentiment_data, trading_dates)
        
        # Wednesday has no data -> should forward fill from Tuesday
        wednesday_result = [r for r in results if r.trading_date.date().isoweekday() == 3][0]
        
        assert wednesday_result.case == AlignmentCase.FORWARD_FILL
        assert wednesday_result.document_count == 0
        # Should carry forward Tuesday's sentiment
        assert wednesday_result.sentiment_score == 0.8
    
    def test_case3_aggregation(self, sample_sentiment_data, trading_dates):
        """Test Case 3: Multiple documents -> aggregate (AIS_t)."""
        aligner = TimeAligner()
        results = aligner.align_to_daily(sample_sentiment_data, trading_dates)
        
        # Monday has 3 documents -> aggregation
        monday_result = [r for r in results if r.trading_date.date().isoweekday() == 1][0]
        
        assert monday_result.case == AlignmentCase.AGGREGATED
        assert monday_result.document_count == 3
        # AIS_t = sum of sentiments = 0.5 + 0.3 + (-0.2) = 0.6
        assert monday_result.sentiment_score == pytest.approx(0.6, rel=0.01)
    
    def test_ais_label_positive(self, sample_sentiment_data, trading_dates):
        """Test AIS label is positive when AIS_t > 0."""
        aligner = TimeAligner()
        results = aligner.align_to_daily(sample_sentiment_data, trading_dates)
        
        monday_result = [r for r in results if r.trading_date.date().isoweekday() == 1][0]
        
        # AIS_t = 0.6 > 0 -> positive
        assert monday_result.ais_label == "positive"
    
    def test_ais_label_negative(self):
        """Test AIS label is negative when AIS_t < 0."""
        est_tz = ZoneInfo("America/New_York")
        
        # Create data with negative sum
        data = pd.DataFrame({
            "created_at": [
                datetime(2025, 1, 13, 10, 0, 0, tzinfo=est_tz),
                datetime(2025, 1, 13, 11, 0, 0, tzinfo=est_tz),
            ],
            "compound": [-0.5, -0.3],
            "positive": [0.1, 0.2],
            "negative": [0.6, 0.5],
            "neutral": [0.3, 0.3],
            "source": ["twitter", "reddit"],
        })
        
        trading_dates = create_trading_date_range("2025-01-13", "2025-01-13")
        
        aligner = TimeAligner()
        results = aligner.align_to_daily(data, trading_dates)
        
        assert results[0].ais_label == "negative"
    
    def test_forward_fill_decay(self):
        """Test that forward fill decays after max_forward_fill_days."""
        aligner = TimeAligner(max_forward_fill_days=3)
        
        est_tz = ZoneInfo("America/New_York")
        
        # Only data on Monday
        data = pd.DataFrame({
            "created_at": [datetime(2025, 1, 13, 10, 0, 0, tzinfo=est_tz)],
            "compound": [0.8],
            "positive": [0.9],
            "negative": [0.1],
            "neutral": [0.0],
            "source": ["twitter"],
        })
        
        # Week of trading dates
        trading_dates = create_trading_date_range("2025-01-13", "2025-01-17")
        
        results = aligner.align_to_daily(data, trading_dates)
        
        # Friday (4 days after Monday) should have decayed sentiment
        friday_result = results[-1]
        assert friday_result.case == AlignmentCase.FORWARD_FILL
        assert abs(friday_result.sentiment_score) < 0.8  # Should be decayed
    
    def test_align_dataframe_output(self, sample_sentiment_data, trading_dates):
        """Test that align_dataframe returns proper DataFrame."""
        aligner = TimeAligner()
        df = aligner.align_dataframe(sample_sentiment_data, trading_dates)
        
        assert isinstance(df, pd.DataFrame)
        assert "trading_date" in df.columns
        assert "sentiment" in df.columns
        assert "alignment_case" in df.columns
        assert "ais_label" in df.columns
        assert len(df) == len(trading_dates)
    
    def test_empty_data_handling(self, trading_dates):
        """Test handling of empty sentiment data."""
        aligner = TimeAligner()
        empty_df = pd.DataFrame()
        
        results = aligner.align_to_daily(empty_df, trading_dates)
        
        assert len(results) == 0


class TestCreateTradingDateRange:
    """Tests for create_trading_date_range function."""
    
    def test_excludes_weekends(self):
        """Test that weekends are excluded by default."""
        dates = create_trading_date_range("2025-01-13", "2025-01-19")
        
        # Mon-Fri = 5 days
        assert len(dates) == 5
        
        for d in dates:
            assert d.weekday() < 5  # 0-4 are Mon-Fri
    
    def test_includes_weekends_when_requested(self):
        """Test including weekends when exclude_weekends=False."""
        dates = create_trading_date_range(
            "2025-01-13", "2025-01-19",
            exclude_weekends=False
        )
        
        # Full 7 days
        assert len(dates) == 7
    
    def test_datetime_input(self):
        """Test with datetime input instead of string."""
        start = datetime(2025, 1, 13)
        end = datetime(2025, 1, 17)
        
        dates = create_trading_date_range(start, end)
        
        assert len(dates) == 5  # Mon-Fri


class TestNormalizeSourceTimestamp:
    """Tests for normalize_source_timestamp convenience function."""
    
    def test_reddit_utc_source(self):
        """Test Reddit source assumes UTC."""
        dt = datetime(2025, 1, 15, 18, 0, 0)  # Naive
        normalized = normalize_source_timestamp(dt, "reddit")
        
        # Should have timezone info
        assert normalized.tzinfo is not None
    
    def test_twitter_utc_source(self):
        """Test Twitter source assumes UTC."""
        timestamp = 1705347600  # Unix timestamp
        normalized = normalize_source_timestamp(timestamp, "twitter")
        
        assert isinstance(normalized, datetime)
        assert normalized.tzinfo is not None
    
    def test_unknown_source_defaults_utc(self):
        """Test unknown source defaults to UTC."""
        dt = datetime(2025, 1, 15, 18, 0, 0)
        normalized = normalize_source_timestamp(dt, "unknown_source")
        
        assert normalized.tzinfo is not None
