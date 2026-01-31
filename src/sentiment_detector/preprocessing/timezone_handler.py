"""
Timezone handling utilities for cross-source timestamp normalization.

Handles the conversion of timestamps from various sources (Reddit, Twitter, News, RSS)
to a standardized timezone (UTC or EST) for consistent alignment.
"""

from datetime import datetime, time, timedelta
from enum import Enum
from typing import Optional, Union
import logging

from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)


class MarketTimezone(str, Enum):
    """Supported market timezones."""
    UTC = "UTC"
    EST = "America/New_York"
    CST = "America/Chicago"
    PST = "America/Los_Angeles"
    GMT = "Europe/London"
    CET = "Europe/Paris"
    JST = "Asia/Tokyo"
    SGT = "Asia/Singapore"


# Standard market close times (EST/EDT)
MARKET_CUTOFF_TIME = time(16, 30)  # 4:30 PM EST - per Kengmegni (2024)


class TimezoneHandler:
    """
    Handles timezone normalization for financial sentiment data.
    
    Following Kengmegni (2024), implements 4:30 PM EST cutoff for
    next-day attribution to prevent look-ahead bias.
    
    Attributes:
        target_timezone: The timezone to normalize all timestamps to (default: EST)
        cutoff_time: Market cutoff time for next-day attribution (default: 4:30 PM)
    """
    
    def __init__(
        self,
        target_timezone: MarketTimezone = MarketTimezone.EST,
        cutoff_time: time = MARKET_CUTOFF_TIME
    ):
        """
        Initialize timezone handler.
        
        Args:
            target_timezone: Target timezone for normalization
            cutoff_time: Daily cutoff time for next-day attribution
        """
        self.target_timezone = target_timezone
        self.target_tz = ZoneInfo(target_timezone.value)
        self.cutoff_time = cutoff_time
        self.utc_tz = ZoneInfo("UTC")
        
    def normalize_timestamp(
        self,
        timestamp: Union[datetime, str, int, float],
        source_timezone: Optional[str] = None
    ) -> datetime:
        """
        Normalize a timestamp to the target timezone.
        
        Args:
            timestamp: Input timestamp (datetime, ISO string, or Unix epoch)
            source_timezone: Source timezone string (e.g., 'UTC', 'America/New_York')
                           If None, assumes UTC or uses existing tzinfo
                           
        Returns:
            datetime: Normalized datetime in target timezone
            
        Raises:
            ValueError: If timestamp format is not recognized
        """
        # Parse timestamp to datetime
        dt = self._parse_timestamp(timestamp)
        
        # Handle naive datetimes
        if dt.tzinfo is None:
            if source_timezone:
                source_tz = ZoneInfo(source_timezone)
                dt = dt.replace(tzinfo=source_tz)
            else:
                # Assume UTC for naive timestamps
                dt = dt.replace(tzinfo=self.utc_tz)
        
        # Convert to target timezone
        return dt.astimezone(self.target_tz)
    
    def _parse_timestamp(self, timestamp: Union[datetime, str, int, float]) -> datetime:
        """Parse various timestamp formats to datetime."""
        if isinstance(timestamp, datetime):
            return timestamp
        elif isinstance(timestamp, str):
            # Try ISO format first
            try:
                return datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except ValueError:
                pass
            # Try common formats
            formats = [
                "%Y-%m-%d %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S",
                "%Y/%m/%d %H:%M:%S",
                "%d-%m-%Y %H:%M:%S",
                "%Y-%m-%d",
            ]
            for fmt in formats:
                try:
                    return datetime.strptime(timestamp, fmt)
                except ValueError:
                    continue
            raise ValueError(f"Unable to parse timestamp: {timestamp}")
        elif isinstance(timestamp, (int, float)):
            # Unix epoch (seconds or milliseconds)
            if timestamp > 1e12:  # Likely milliseconds
                timestamp = timestamp / 1000
            return datetime.fromtimestamp(timestamp, tz=self.utc_tz)
        else:
            raise ValueError(f"Unsupported timestamp type: {type(timestamp)}")
    
    def get_trading_date(self, timestamp: Union[datetime, str, int, float]) -> datetime:
        """
        Get the trading date for a given timestamp.
        
        Implements the 4:30 PM EST cutoff from Kengmegni (2024):
        - Timestamps before cutoff → same day
        - Timestamps after cutoff → next trading day
        
        Args:
            timestamp: Input timestamp
            
        Returns:
            datetime: Trading date (date only, at midnight of target timezone)
        """
        normalized = self.normalize_timestamp(timestamp)
        
        # Check if after market cutoff
        if normalized.time() > self.cutoff_time:
            # Attribute to next trading day
            trading_date = normalized.date() + timedelta(days=1)
        else:
            trading_date = normalized.date()
        
        # Handle weekends - move to next Monday
        trading_date = self._adjust_for_weekends(trading_date)
        
        # Return as datetime at midnight in target timezone
        return datetime.combine(trading_date, time.min, tzinfo=self.target_tz)
    
    def _adjust_for_weekends(self, date: datetime) -> datetime:
        """Adjust weekend dates to the following Monday."""
        if hasattr(date, 'date'):
            date = date.date()
        
        # Monday = 0, Sunday = 6
        weekday = date.weekday()
        
        if weekday == 5:  # Saturday
            return date + timedelta(days=2)
        elif weekday == 6:  # Sunday
            return date + timedelta(days=1)
        
        return date
    
    def is_market_hours(
        self,
        timestamp: Union[datetime, str, int, float],
        market_open: time = time(9, 30),
        market_close: time = time(16, 0)
    ) -> bool:
        """
        Check if timestamp falls within regular market hours.
        
        Args:
            timestamp: Input timestamp
            market_open: Market open time (default: 9:30 AM EST)
            market_close: Market close time (default: 4:00 PM EST)
            
        Returns:
            bool: True if within market hours
        """
        normalized = self.normalize_timestamp(timestamp)
        current_time = normalized.time()
        
        # Check weekday
        if normalized.weekday() >= 5:  # Saturday or Sunday
            return False
        
        return market_open <= current_time <= market_close
    
    def get_interval_bounds(
        self,
        trading_date: datetime,
        interval_type: str = "daily"
    ) -> tuple[datetime, datetime]:
        """
        Get the start and end bounds for a trading interval.
        
        Args:
            trading_date: The trading date to get bounds for
            interval_type: "daily", "hourly", or "weekly"
            
        Returns:
            tuple: (start_datetime, end_datetime) in target timezone
        """
        if hasattr(trading_date, 'date'):
            date = trading_date.date()
        else:
            date = trading_date
            
        if interval_type == "daily":
            # Previous cutoff to current cutoff
            start = datetime.combine(date - timedelta(days=1), self.cutoff_time, tzinfo=self.target_tz)
            end = datetime.combine(date, self.cutoff_time, tzinfo=self.target_tz)
        elif interval_type == "hourly":
            # Use the full hour of the provided datetime
            hour_start = trading_date.replace(minute=0, second=0, microsecond=0)
            start = hour_start
            end = hour_start + timedelta(hours=1)
        elif interval_type == "weekly":
            # Monday to Friday, cutoff to cutoff
            # Find the Monday of the week
            days_since_monday = date.weekday()
            monday = date - timedelta(days=days_since_monday)
            friday = monday + timedelta(days=4)
            start = datetime.combine(monday - timedelta(days=3), self.cutoff_time, tzinfo=self.target_tz)  # Previous Friday cutoff
            end = datetime.combine(friday, self.cutoff_time, tzinfo=self.target_tz)
        else:
            raise ValueError(f"Unknown interval type: {interval_type}")
        
        return start, end


def normalize_source_timestamp(
    timestamp: Union[datetime, str, int, float],
    source: str
) -> datetime:
    """
    Convenience function to normalize timestamps from known sources.
    
    Args:
        timestamp: Input timestamp
        source: Source name ('reddit', 'twitter', 'news', 'rss', 'kaggle')
        
    Returns:
        datetime: Normalized timestamp in EST
    """
    # Source-specific timezone assumptions
    source_timezones = {
        "reddit": "UTC",
        "twitter": "UTC",
        "news": "UTC",  # Most news APIs return UTC
        "rss": "UTC",
        "kaggle": "UTC",
        "yahoo_finance": "America/New_York",
    }
    
    source_tz = source_timezones.get(source.lower(), "UTC")
    
    handler = TimezoneHandler()
    return handler.normalize_timestamp(timestamp, source_timezone=source_tz)
