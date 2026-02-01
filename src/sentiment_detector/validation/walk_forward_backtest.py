"""
Walk-Forward Backtesting Framework.

This module implements walk-forward validation for the regime detection model,
testing against known market events:
- COVID crash (March 2020)
- Crypto Winter (2022)
- GameStop squeeze (January 2021)

Walk-forward prevents look-ahead bias by:
1. Training on past data only
2. Testing on future windows
3. Rolling the window forward

References:
- Bailey et al. (2014): Walk-forward validation for financial ML
- López de Prado (2018): Purged K-Fold cross-validation
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple, Callable, Any
from enum import Enum
from datetime import datetime, timedelta
import logging

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score,
    confusion_matrix,
    classification_report,
)

logger = logging.getLogger(__name__)


@dataclass
class MarketEvent:
    """
    A known market event for targeted backtesting.
    
    Attributes:
        name: Event name
        start_date: Event start date
        end_date: Event end date
        expected_regime: Expected regime during event
        pre_event_days: Days before event to analyze for warning signals
        post_event_days: Days after for recovery analysis
        description: Event description
    """
    name: str
    start_date: datetime
    end_date: datetime
    expected_regime: str  # 'high_volatility', 'elevated', 'crisis'
    pre_event_days: int = 10
    post_event_days: int = 30
    description: str = ""


# Pre-defined market events for backtesting
COVID_CRASH = MarketEvent(
    name="COVID-19 Crash",
    start_date=datetime(2020, 2, 20),
    end_date=datetime(2020, 3, 23),
    expected_regime="high_volatility",
    pre_event_days=14,
    post_event_days=60,
    description="Market crash due to COVID-19 pandemic fears. VIX spiked to 82.69."
)

GAMESTOP_SQUEEZE = MarketEvent(
    name="GameStop Short Squeeze",
    start_date=datetime(2021, 1, 25),
    end_date=datetime(2021, 2, 5),
    expected_regime="elevated",
    pre_event_days=7,
    post_event_days=30,
    description="Retail investor-driven short squeeze on GME. VIX elevated."
)

CRYPTO_WINTER_2022 = MarketEvent(
    name="Crypto Winter 2022",
    start_date=datetime(2022, 5, 1),
    end_date=datetime(2022, 12, 31),
    expected_regime="elevated",
    pre_event_days=30,
    post_event_days=30,
    description="Prolonged crypto market downturn following Terra/Luna collapse."
)

FTX_COLLAPSE = MarketEvent(
    name="FTX Collapse",
    start_date=datetime(2022, 11, 2),
    end_date=datetime(2022, 11, 20),
    expected_regime="high_volatility",
    pre_event_days=7,
    post_event_days=30,
    description="FTX exchange collapse and contagion effects."
)

SVB_COLLAPSE = MarketEvent(
    name="SVB Bank Collapse",
    start_date=datetime(2023, 3, 8),
    end_date=datetime(2023, 3, 20),
    expected_regime="elevated",
    pre_event_days=5,
    post_event_days=30,
    description="Silicon Valley Bank failure and regional banking crisis."
)

# Collection of key events
KEY_MARKET_EVENTS = [
    COVID_CRASH,
    GAMESTOP_SQUEEZE,
    CRYPTO_WINTER_2022,
    FTX_COLLAPSE,
    SVB_COLLAPSE,
]


@dataclass
class BacktestWindow:
    """A single train/test window for walk-forward validation."""
    window_id: int
    train_start: datetime
    train_end: datetime
    test_start: datetime
    test_end: datetime
    train_size: int = 0
    test_size: int = 0


@dataclass
class WindowResult:
    """Results from a single backtest window."""
    window: BacktestWindow
    accuracy: float
    precision: float
    recall: float
    f1: float
    confusion_matrix: np.ndarray
    predictions: pd.Series
    true_labels: pd.Series
    regime_distribution: Dict[str, float]


@dataclass
class EventBacktestResult:
    """Results from backtesting against a specific market event."""
    event: MarketEvent
    
    # Detection metrics
    detected_pre_event: bool  # Did model detect warning signals?
    warning_days: int  # How many days before event onset?
    regime_during_event: str  # What regime was detected?
    regime_accuracy: float  # Accuracy during event period
    
    # Transition analysis
    pre_event_regime: str
    transition_date: Optional[datetime]
    recovery_date: Optional[datetime]
    
    # Performance metrics during event
    precision: float
    recall: float
    f1: float
    
    # Evidence
    evidence: List[str] = field(default_factory=list)


@dataclass
class WalkForwardResult:
    """Complete results from walk-forward backtesting."""
    
    # Overall metrics
    overall_accuracy: float
    overall_precision: float
    overall_recall: float
    overall_f1: float
    
    # Window-by-window results
    window_results: List[WindowResult]
    
    # Event-specific results
    event_results: Dict[str, EventBacktestResult]
    
    # Aggregate statistics
    avg_window_accuracy: float
    std_window_accuracy: float
    min_window_accuracy: float
    max_window_accuracy: float
    
    # Configuration
    train_window_days: int
    test_window_days: int
    step_days: int
    n_windows: int
    
    def summary(self) -> str:
        """Generate a summary report."""
        lines = [
            "=" * 60,
            "WALK-FORWARD BACKTESTING RESULTS",
            "=" * 60,
            "",
            f"Configuration:",
            f"  Train window: {self.train_window_days} days",
            f"  Test window: {self.test_window_days} days",
            f"  Step size: {self.step_days} days",
            f"  Total windows: {self.n_windows}",
            "",
            f"Overall Metrics:",
            f"  Accuracy: {self.overall_accuracy:.4f}",
            f"  Precision: {self.overall_precision:.4f}",
            f"  Recall: {self.overall_recall:.4f}",
            f"  F1 Score: {self.overall_f1:.4f}",
            "",
            f"Window Statistics:",
            f"  Avg Accuracy: {self.avg_window_accuracy:.4f} ± {self.std_window_accuracy:.4f}",
            f"  Range: [{self.min_window_accuracy:.4f}, {self.max_window_accuracy:.4f}]",
        ]
        
        if self.event_results:
            lines.extend(["", "=" * 60, "EVENT DETECTION RESULTS", "=" * 60])
            for event_name, result in self.event_results.items():
                lines.extend([
                    f"",
                    f"📌 {event_name}",
                    f"   Detected pre-event: {'✅' if result.detected_pre_event else '❌'}",
                    f"   Warning days: {result.warning_days}",
                    f"   Regime during event: {result.regime_during_event}",
                    f"   Accuracy during event: {result.regime_accuracy:.2%}",
                ])
                for evidence in result.evidence:
                    lines.append(f"   • {evidence}")
        
        return "\n".join(lines)


class WalkForwardBacktester:
    """
    Walk-forward backtesting framework for regime detection models.
    
    Example:
        >>> backtester = WalkForwardBacktester(
        ...     train_window_days=252,  # 1 year
        ...     test_window_days=21,    # 1 month
        ...     step_days=21,           # Monthly rolling
        ... )
        >>> results = backtester.run(
        ...     features=feature_df,
        ...     labels=regime_series,
        ...     model_fn=lambda X, y: train_model(X, y),
        ...     predict_fn=lambda model, X: model.predict(X),
        ... )
        >>> print(results.summary())
    """
    
    def __init__(
        self,
        train_window_days: int = 252,  # 1 trading year
        test_window_days: int = 21,    # 1 trading month
        step_days: int = 21,           # Monthly step
        purge_days: int = 5,           # Gap to prevent leakage
        embargo_days: int = 5,         # Post-train embargo
        events: Optional[List[MarketEvent]] = None,
    ):
        """
        Initialize walk-forward backtester.
        
        Args:
            train_window_days: Size of training window in trading days
            test_window_days: Size of test window in trading days
            step_days: Step size for rolling window
            purge_days: Days to purge between train and test
            embargo_days: Days to embargo at end of test
            events: Market events to test against
        """
        self.train_window_days = train_window_days
        self.test_window_days = test_window_days
        self.step_days = step_days
        self.purge_days = purge_days
        self.embargo_days = embargo_days
        self.events = events or KEY_MARKET_EVENTS
        
        logger.info(
            f"WalkForwardBacktester initialized: "
            f"train={train_window_days}d, test={test_window_days}d, step={step_days}d"
        )
    
    def generate_windows(
        self, 
        data: pd.DataFrame
    ) -> List[BacktestWindow]:
        """
        Generate walk-forward windows from data.
        
        Args:
            data: DataFrame with datetime index
            
        Returns:
            List of BacktestWindow objects
        """
        windows = []
        dates = data.index.sort_values()
        
        # Calculate minimum data needed
        min_required = self.train_window_days + self.purge_days + self.test_window_days
        if len(dates) < min_required:
            raise ValueError(
                f"Insufficient data: {len(dates)} days, need {min_required}"
            )
        
        # Generate windows
        window_id = 0
        train_start_idx = 0
        
        while True:
            train_end_idx = train_start_idx + self.train_window_days - 1
            test_start_idx = train_end_idx + self.purge_days + 1
            test_end_idx = test_start_idx + self.test_window_days - 1
            
            # Check if we have enough data
            if test_end_idx >= len(dates):
                break
            
            window = BacktestWindow(
                window_id=window_id,
                train_start=dates[train_start_idx],
                train_end=dates[train_end_idx],
                test_start=dates[test_start_idx],
                test_end=dates[test_end_idx],
                train_size=self.train_window_days,
                test_size=self.test_window_days,
            )
            windows.append(window)
            
            window_id += 1
            train_start_idx += self.step_days
        
        logger.info(f"Generated {len(windows)} backtest windows")
        return windows
    
    def run(
        self,
        features: pd.DataFrame,
        labels: pd.Series,
        model_fn: Callable[[pd.DataFrame, pd.Series], Any],
        predict_fn: Callable[[Any, pd.DataFrame], np.ndarray],
        label_encoder: Optional[Dict[str, int]] = None,
    ) -> WalkForwardResult:
        """
        Run walk-forward backtesting.
        
        Args:
            features: Feature DataFrame with datetime index
            labels: Regime labels with datetime index
            model_fn: Function to train model: (X_train, y_train) -> model
            predict_fn: Function to predict: (model, X_test) -> predictions
            label_encoder: Optional mapping from string labels to integers
            
        Returns:
            WalkForwardResult with all metrics
        """
        # Align features and labels
        common_idx = features.index.intersection(labels.index)
        features = features.loc[common_idx]
        labels = labels.loc[common_idx]
        
        # Generate windows
        windows = self.generate_windows(features)
        
        if len(windows) == 0:
            raise ValueError("No valid windows generated")
        
        # Run backtests
        window_results = []
        all_predictions = []
        all_true = []
        
        for window in windows:
            logger.debug(f"Processing window {window.window_id}")
            
            # Get train/test splits
            train_mask = (features.index >= window.train_start) & \
                        (features.index <= window.train_end)
            test_mask = (features.index >= window.test_start) & \
                       (features.index <= window.test_end)
            
            X_train = features.loc[train_mask]
            y_train = labels.loc[train_mask]
            X_test = features.loc[test_mask]
            y_test = labels.loc[test_mask]
            
            if len(X_train) == 0 or len(X_test) == 0:
                continue
            
            # Train and predict
            try:
                model = model_fn(X_train, y_train)
                predictions = predict_fn(model, X_test)
            except Exception as e:
                logger.warning(f"Window {window.window_id} failed: {e}")
                continue
            
            # Convert to series
            pred_series = pd.Series(predictions, index=X_test.index)
            
            # Calculate metrics
            result = self._evaluate_window(window, pred_series, y_test)
            window_results.append(result)
            
            all_predictions.extend(predictions)
            all_true.extend(y_test.values)
        
        # Calculate overall metrics
        all_predictions = np.array(all_predictions)
        all_true = np.array(all_true)
        
        # Event-specific testing
        event_results = {}
        for event in self.events:
            try:
                event_result = self._evaluate_event(
                    event, features, labels, model_fn, predict_fn
                )
                event_results[event.name] = event_result
            except Exception as e:
                logger.warning(f"Event {event.name} evaluation failed: {e}")
        
        # Aggregate window statistics
        window_accuracies = [r.accuracy for r in window_results]
        
        return WalkForwardResult(
            overall_accuracy=accuracy_score(all_true, all_predictions) if len(all_true) > 0 else 0,
            overall_precision=precision_score(all_true, all_predictions, average='weighted', zero_division=0),
            overall_recall=recall_score(all_true, all_predictions, average='weighted', zero_division=0),
            overall_f1=f1_score(all_true, all_predictions, average='weighted', zero_division=0),
            window_results=window_results,
            event_results=event_results,
            avg_window_accuracy=np.mean(window_accuracies) if window_accuracies else 0,
            std_window_accuracy=np.std(window_accuracies) if window_accuracies else 0,
            min_window_accuracy=np.min(window_accuracies) if window_accuracies else 0,
            max_window_accuracy=np.max(window_accuracies) if window_accuracies else 0,
            train_window_days=self.train_window_days,
            test_window_days=self.test_window_days,
            step_days=self.step_days,
            n_windows=len(windows),
        )
    
    def _evaluate_window(
        self,
        window: BacktestWindow,
        predictions: pd.Series,
        true_labels: pd.Series,
    ) -> WindowResult:
        """Evaluate a single backtest window."""
        # Align
        common = predictions.index.intersection(true_labels.index)
        pred = predictions.loc[common]
        true = true_labels.loc[common]
        
        # Calculate metrics
        accuracy = accuracy_score(true, pred)
        precision = precision_score(true, pred, average='weighted', zero_division=0)
        recall = recall_score(true, pred, average='weighted', zero_division=0)
        f1 = f1_score(true, pred, average='weighted', zero_division=0)
        cm = confusion_matrix(true, pred)
        
        # Regime distribution
        regime_dist = {}
        for regime in pred.unique():
            regime_dist[str(regime)] = (pred == regime).mean()
        
        return WindowResult(
            window=window,
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1=f1,
            confusion_matrix=cm,
            predictions=pred,
            true_labels=true,
            regime_distribution=regime_dist,
        )
    
    def _evaluate_event(
        self,
        event: MarketEvent,
        features: pd.DataFrame,
        labels: pd.Series,
        model_fn: Callable,
        predict_fn: Callable,
    ) -> EventBacktestResult:
        """
        Evaluate model performance for a specific market event.
        
        Uses expanding window trained on all data before the event
        to predict during the event.
        """
        event_start = pd.Timestamp(event.start_date)
        event_end = pd.Timestamp(event.end_date)
        
        # Pre-event window for training
        train_end = event_start - timedelta(days=1)
        train_start = train_end - timedelta(days=self.train_window_days)
        
        # Check if we have data
        if train_start < features.index.min():
            raise ValueError(f"Insufficient data before event {event.name}")
        
        # Training data (before event)
        train_mask = (features.index >= train_start) & (features.index <= train_end)
        X_train = features.loc[train_mask]
        y_train = labels.loc[train_mask]
        
        # Event period data
        event_mask = (features.index >= event_start) & (features.index <= event_end)
        X_event = features.loc[event_mask]
        y_event = labels.loc[event_mask]
        
        # Pre-event period (for early warning detection)
        pre_event_start = event_start - timedelta(days=event.pre_event_days)
        pre_event_mask = (features.index >= pre_event_start) & (features.index < event_start)
        X_pre_event = features.loc[pre_event_mask]
        y_pre_event = labels.loc[pre_event_mask] if len(labels.loc[pre_event_mask]) > 0 else pd.Series()
        
        if len(X_train) == 0 or len(X_event) == 0:
            raise ValueError(f"No data for event {event.name}")
        
        # Train model
        model = model_fn(X_train, y_train)
        
        # Predict during event
        predictions_event = predict_fn(model, X_event)
        pred_event_series = pd.Series(predictions_event, index=X_event.index)
        
        # Predict pre-event (for early warning)
        if len(X_pre_event) > 0:
            predictions_pre = predict_fn(model, X_pre_event)
            pred_pre_series = pd.Series(predictions_pre, index=X_pre_event.index)
        else:
            pred_pre_series = pd.Series()
        
        # Analyze results
        evidence = []
        
        # What regime was detected during event?
        regime_during = pd.Series(predictions_event).mode()[0] if len(predictions_event) > 0 else "unknown"
        
        # Did it match expected?
        expected_matches = [regime_during] if str(regime_during) == event.expected_regime else []
        
        # Early warning detection
        detected_pre_event = False
        warning_days = 0
        transition_date = None
        
        if len(pred_pre_series) > 0:
            # Look for regime change to elevated/high_volatility before event
            high_risk_regimes = ['elevated', 'high_volatility', 'risk_off', 'crisis']
            for date in pred_pre_series.index:
                regime = pred_pre_series[date]
                if str(regime).lower() in [r.lower() for r in high_risk_regimes]:
                    detected_pre_event = True
                    transition_date = date
                    warning_days = (event_start - date).days
                    evidence.append(f"Detected regime shift to '{regime}' {warning_days} days before event")
                    break
        
        # Calculate metrics for event period
        if len(y_event) > 0:
            accuracy = accuracy_score(y_event, predictions_event)
            precision = precision_score(y_event, predictions_event, average='weighted', zero_division=0)
            recall = recall_score(y_event, predictions_event, average='weighted', zero_division=0)
            f1 = f1_score(y_event, predictions_event, average='weighted', zero_division=0)
        else:
            accuracy = precision = recall = f1 = 0
        
        # Pre-event regime
        if len(pred_pre_series) > 0:
            pre_event_regime = pd.Series(pred_pre_series.values).mode()[0]
        else:
            pre_event_regime = "unknown"
        
        # Add more evidence
        evidence.append(f"Detected regime during event: {regime_during}")
        evidence.append(f"Expected regime: {event.expected_regime}")
        if accuracy > 0.7:
            evidence.append(f"High accuracy during event: {accuracy:.1%}")
        
        return EventBacktestResult(
            event=event,
            detected_pre_event=detected_pre_event,
            warning_days=warning_days,
            regime_during_event=str(regime_during),
            regime_accuracy=accuracy,
            pre_event_regime=str(pre_event_regime),
            transition_date=transition_date,
            recovery_date=None,  # Would need post-event analysis
            precision=precision,
            recall=recall,
            f1=f1,
            evidence=evidence,
        )
    
    def run_event_only(
        self,
        features: pd.DataFrame,
        labels: pd.Series,
        model_fn: Callable,
        predict_fn: Callable,
        events: Optional[List[MarketEvent]] = None,
    ) -> Dict[str, EventBacktestResult]:
        """
        Run backtesting only for specific market events.
        
        Useful when you want to quickly test event detection
        without full walk-forward validation.
        """
        events = events or self.events
        results = {}
        
        for event in events:
            try:
                result = self._evaluate_event(
                    event, features, labels, model_fn, predict_fn
                )
                results[event.name] = result
                logger.info(f"Event '{event.name}': warning_days={result.warning_days}, accuracy={result.regime_accuracy:.2%}")
            except Exception as e:
                logger.warning(f"Event '{event.name}' failed: {e}")
        
        return results


def create_synthetic_crisis_data(
    n_days: int = 1000,
    crisis_periods: Optional[List[Tuple[int, int, str]]] = None,
) -> Tuple[pd.DataFrame, pd.Series]:
    """
    Create synthetic data with crisis periods for testing.
    
    Args:
        n_days: Total number of days
        crisis_periods: List of (start_day, end_day, regime) tuples
        
    Returns:
        Tuple of (features_df, labels_series)
    """
    np.random.seed(42)
    dates = pd.date_range(start='2019-01-01', periods=n_days, freq='D')
    
    # Default crisis periods
    if crisis_periods is None:
        crisis_periods = [
            (300, 350, 'high_volatility'),  # Crisis 1
            (600, 620, 'elevated'),         # Crisis 2
            (800, 850, 'high_volatility'),  # Crisis 3
        ]
    
    # Generate features
    base_vol = 15 + np.random.randn(n_days) * 2
    sentiment = 0.1 + np.random.randn(n_days) * 0.3
    tci = 0.5 + np.random.randn(n_days) * 0.1
    
    # Add crisis signals
    labels = ['normal'] * n_days
    for start, end, regime in crisis_periods:
        if end > n_days:
            continue
        # Modify features during crisis
        base_vol[start:end] += 20
        sentiment[start-10:end] -= 0.5  # Sentiment drops before crisis
        tci[start:end] -= 0.2  # TCI drops during crisis
        labels[start:end] = [regime] * (end - start)
    
    features = pd.DataFrame({
        'volatility': base_vol,
        'sentiment': sentiment,
        'tci': tci,
        'momentum': np.random.randn(n_days) * 0.1,
        'volume': 1 + np.random.rand(n_days) * 0.5,
    }, index=dates)
    
    labels = pd.Series(labels, index=dates, name='regime')
    
    return features, labels
