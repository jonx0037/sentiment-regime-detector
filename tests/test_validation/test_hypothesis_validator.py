"""
Tests for hypothesis validation framework.

Tests the H1, H2, H3 hypothesis validators with synthetic data.
"""

import pytest
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from src.sentiment_detector.validation.hypothesis_validator import (
    HypothesisValidator,
    HypothesisResult,
    H1Result,
    H2Result,
    H3Result,
    LeadLagResult,
    GrangerResult,
    generate_hypothesis_report,
)


class TestHypothesisValidator:
    """Tests for HypothesisValidator class."""
    
    @pytest.fixture
    def validator(self):
        """Create a validator instance."""
        return HypothesisValidator(
            significance_level=0.05,
            max_lag_days=10,
            min_effect_size=0.3
        )
    
    @pytest.fixture
    def date_range(self):
        """Create a date range for testing."""
        return pd.date_range(start='2020-01-01', periods=500, freq='D')
    
    @pytest.fixture
    def synthetic_sentiment_leading_vix(self, date_range):
        """
        Create synthetic data where sentiment leads VIX by 3 days.
        
        This tests H1 (Leading Indicator Hypothesis).
        """
        np.random.seed(42)
        n = len(date_range)
        
        # Create base signal
        base_signal = np.sin(np.linspace(0, 4 * np.pi, n)) + np.random.randn(n) * 0.3
        
        # Sentiment leads (at time t)
        sentiment = pd.Series(base_signal, index=date_range, name='sentiment')
        
        # VIX lags by 3 days (inverse relationship - negative sentiment → high VIX)
        vix_base = -base_signal * 5 + 20  # VIX around 20, higher when sentiment low
        vix = pd.Series(
            np.roll(vix_base, 3) + np.random.randn(n) * 1,  # 3-day lag
            index=date_range,
            name='vix'
        )
        vix = vix.clip(10, 80)  # VIX bounds
        
        return sentiment, vix
    
    @pytest.fixture
    def synthetic_no_lead_lag(self, date_range):
        """Create independent sentiment and VIX series."""
        np.random.seed(42)
        n = len(date_range)
        
        sentiment = pd.Series(
            np.random.randn(n),
            index=date_range,
            name='sentiment'
        )
        vix = pd.Series(
            np.random.randn(n) * 5 + 20,
            index=date_range,
            name='vix'
        )
        
        return sentiment, vix
    
    @pytest.fixture
    def synthetic_divergence_before_transition(self, date_range):
        """
        Create synthetic multi-asset sentiment with divergence before transitions.
        
        This tests H2 (Divergence Signal Hypothesis).
        """
        np.random.seed(42)
        n = len(date_range)
        
        # Create regime series with transitions
        regimes = ['stable'] * n
        transition_points = [100, 200, 300, 400]
        
        for tp in transition_points:
            if tp < n:
                regimes[tp:min(tp + 20, n)] = ['transition'] * min(20, n - tp)
        
        regime_series = pd.Series(regimes, index=date_range)
        
        # Create asset sentiment
        # During stable: assets move together (low divergence)
        # Before transition: assets diverge (high divergence)
        
        sentiment_data = {}
        base_sentiment = np.sin(np.linspace(0, 4 * np.pi, n))
        
        for i, asset in enumerate(['equities', 'bonds', 'crypto', 'commodities']):
            asset_sentiment = base_sentiment.copy()
            
            # Add divergence before transition points
            for tp in transition_points:
                if tp < n:
                    # 5 days before transition: increase divergence
                    start_diverge = max(0, tp - 5)
                    divergence = (i - 1.5) * 0.5  # Different direction for each asset
                    asset_sentiment[start_diverge:tp] += divergence
            
            # Add noise
            asset_sentiment += np.random.randn(n) * 0.1
            sentiment_data[asset] = asset_sentiment
        
        sentiment_df = pd.DataFrame(sentiment_data, index=date_range)
        
        return sentiment_df, regime_series
    
    @pytest.fixture
    def synthetic_connectedness_data(self, date_range):
        """
        Create synthetic TCI data with pattern:
        - High TCI during stable regimes
        - Decreasing TCI before crashes
        
        This tests H3 (Network Effect Hypothesis).
        """
        np.random.seed(42)
        n = len(date_range)
        
        # Create regime series
        regimes = ['stable'] * n
        crash_dates = [
            datetime(2020, 3, 15),   # COVID crash
            datetime(2020, 10, 28),  # Election volatility
        ]
        
        # Convert to date indices
        crash_indices = []
        for crash in crash_dates:
            crash_dt = pd.Timestamp(crash)
            if crash_dt in date_range:
                crash_indices.append(date_range.get_loc(crash_dt))
            else:
                # Find closest date
                for i, d in enumerate(date_range):
                    if d >= crash_dt:
                        crash_indices.append(i)
                        break
        
        for idx in crash_indices:
            if idx < n:
                regimes[idx:min(idx + 30, n)] = ['crash'] * min(30, n - idx)
        
        regime_series = pd.Series(regimes, index=date_range)
        
        # Create TCI
        tci = np.ones(n) * 0.5  # Base TCI = 0.5
        
        # Higher TCI during stable periods
        for i, r in enumerate(regimes):
            if r == 'stable':
                tci[i] += np.random.randn() * 0.05 + 0.1
            else:
                tci[i] += np.random.randn() * 0.05 - 0.1
        
        # Decreasing TCI before crashes
        for idx in crash_indices:
            if idx >= 10:
                decline = np.linspace(0, -0.15, 10)
                tci[idx - 10:idx] += decline
        
        tci = np.clip(tci, 0, 1)
        tci_series = pd.Series(tci, index=date_range, name='tci')
        
        return tci_series, regime_series, crash_dates


class TestH1Validation(TestHypothesisValidator):
    """Tests for H1 (Leading Indicator Hypothesis)."""
    
    def test_h1_detects_lead_lag(
        self, validator, synthetic_sentiment_leading_vix
    ):
        """Test that H1 detects sentiment leading VIX."""
        sentiment, vix = synthetic_sentiment_leading_vix
        
        result = validator.validate_h1(sentiment, vix)
        
        assert isinstance(result, H1Result)
        assert result.lead_lag is not None
        # Sentiment should lead (positive lag) by approximately 3 days
        assert 1 <= result.lead_lag.optimal_lag <= 5
    
    def test_h1_no_relationship(
        self, validator, synthetic_no_lead_lag
    ):
        """Test that H1 correctly identifies no relationship."""
        sentiment, vix = synthetic_no_lead_lag
        
        result = validator.validate_h1(sentiment, vix)
        
        assert isinstance(result, H1Result)
        # Should not find strong relationship
        assert result.lead_lag is None or abs(result.lead_lag.max_correlation) < 0.3
    
    def test_h1_summary_format(
        self, validator, synthetic_sentiment_leading_vix
    ):
        """Test that H1 result summary is properly formatted."""
        sentiment, vix = synthetic_sentiment_leading_vix
        
        result = validator.validate_h1(sentiment, vix)
        summary = result.summary()
        
        assert "H1" in summary
        assert "Leading Indicator" in summary
        assert "Lead-Lag Analysis" in summary
    
    def test_h1_insufficient_data(self, validator):
        """Test that H1 handles insufficient data gracefully."""
        dates = pd.date_range(start='2020-01-01', periods=10, freq='D')
        sentiment = pd.Series(np.random.randn(10), index=dates)
        vix = pd.Series(np.random.randn(10) * 5 + 20, index=dates)
        
        result = validator.validate_h1(sentiment, vix)
        
        assert result.result == HypothesisResult.INCONCLUSIVE
        assert any("Insufficient" in e for e in result.evidence)


class TestH2Validation(TestHypothesisValidator):
    """Tests for H2 (Divergence Signal Hypothesis)."""
    
    def test_h2_detects_divergence_before_transition(
        self, validator, synthetic_divergence_before_transition
    ):
        """Test that H2 detects divergence before regime transitions."""
        sentiment_df, regime_series = synthetic_divergence_before_transition
        
        result = validator.validate_h2(sentiment_df, regime_series)
        
        assert isinstance(result, H2Result)
        # Pre-transition divergence should be higher
        if result.pre_transition_divergence and result.stable_period_divergence:
            assert result.divergence_ratio > 1.0
    
    def test_h2_calculates_effect_size(
        self, validator, synthetic_divergence_before_transition
    ):
        """Test that H2 calculates Cohen's d effect size."""
        sentiment_df, regime_series = synthetic_divergence_before_transition
        
        result = validator.validate_h2(sentiment_df, regime_series)
        
        if result.effect_size is not None:
            # Effect size should be a reasonable value
            assert -5 < result.effect_size < 5
    
    def test_h2_statistical_test(
        self, validator, synthetic_divergence_before_transition
    ):
        """Test that H2 performs t-test."""
        sentiment_df, regime_series = synthetic_divergence_before_transition
        
        result = validator.validate_h2(sentiment_df, regime_series)
        
        if result.p_value is not None:
            assert 0 <= result.p_value <= 1
    
    def test_h2_summary_format(
        self, validator, synthetic_divergence_before_transition
    ):
        """Test that H2 result summary is properly formatted."""
        sentiment_df, regime_series = synthetic_divergence_before_transition
        
        result = validator.validate_h2(sentiment_df, regime_series)
        summary = result.summary()
        
        assert "H2" in summary
        assert "Divergence" in summary


class TestH3Validation(TestHypothesisValidator):
    """Tests for H3 (Network Effect Hypothesis)."""
    
    def test_h3_detects_tci_regime_pattern(
        self, validator, synthetic_connectedness_data
    ):
        """Test that H3 detects TCI differences across regimes."""
        tci_series, regime_series, crash_dates = synthetic_connectedness_data
        
        result = validator.validate_h3(tci_series, regime_series, crash_dates)
        
        assert isinstance(result, H3Result)
        if result.stable_regime_tci and result.transition_tci:
            # Stable TCI should be higher than crash TCI
            assert result.stable_regime_tci > result.transition_tci
    
    def test_h3_pre_crash_decline(
        self, validator, synthetic_connectedness_data
    ):
        """Test that H3 detects TCI decline before crashes."""
        tci_series, regime_series, crash_dates = synthetic_connectedness_data
        
        result = validator.validate_h3(tci_series, regime_series, crash_dates)
        
        if result.pre_crash_tci_change is not None:
            # TCI should decrease before crashes
            assert result.pre_crash_tci_change < 0
    
    def test_h3_anova_test(
        self, validator, synthetic_connectedness_data
    ):
        """Test that H3 performs ANOVA test."""
        tci_series, regime_series, _ = synthetic_connectedness_data
        
        result = validator.validate_h3(tci_series, regime_series)
        
        if result.anova_p is not None:
            assert 0 <= result.anova_p <= 1
    
    def test_h3_summary_format(
        self, validator, synthetic_connectedness_data
    ):
        """Test that H3 result summary is properly formatted."""
        tci_series, regime_series, crash_dates = synthetic_connectedness_data
        
        result = validator.validate_h3(tci_series, regime_series, crash_dates)
        summary = result.summary()
        
        assert "H3" in summary
        assert "Network Effect" in summary


class TestLeadLagAnalysis(TestHypothesisValidator):
    """Tests for lead-lag cross-correlation analysis."""
    
    def test_lead_lag_result_structure(self, validator, date_range):
        """Test LeadLagResult dataclass structure."""
        np.random.seed(42)
        n = len(date_range)
        
        x = np.sin(np.linspace(0, 4 * np.pi, n))
        y = np.roll(x, 5)  # y lags x by 5
        
        result = validator._compute_lead_lag(x, y)
        
        assert isinstance(result, LeadLagResult)
        assert hasattr(result, 'optimal_lag')
        assert hasattr(result, 'max_correlation')
        assert hasattr(result, 'correlations_by_lag')
        assert hasattr(result, 'p_value')
        assert hasattr(result, 'is_significant')
        assert hasattr(result, 'confidence_interval')
    
    def test_lead_lag_detects_positive_lag(self, validator, date_range):
        """Test detection of x leading y."""
        np.random.seed(42)
        n = len(date_range)
        
        x = np.sin(np.linspace(0, 4 * np.pi, n))
        y = np.roll(x, 5) + np.random.randn(n) * 0.1  # y lags x by 5
        
        result = validator._compute_lead_lag(x, y)
        
        # Positive lag means x leads y
        assert result.optimal_lag > 0
        assert 3 <= result.optimal_lag <= 7  # Should be around 5
    
    def test_lead_lag_correlation_bounds(self, validator, date_range):
        """Test that correlations are bounded."""
        np.random.seed(42)
        n = len(date_range)
        
        x = np.random.randn(n)
        y = np.random.randn(n)
        
        result = validator._compute_lead_lag(x, y)
        
        for lag, corr in result.correlations_by_lag.items():
            assert -1 <= corr <= 1


class TestGrangerCausality(TestHypothesisValidator):
    """Tests for Granger causality analysis."""
    
    def test_granger_result_structure(self, validator):
        """Test GrangerResult dataclass structure."""
        result = GrangerResult(
            f_statistic=5.0,
            p_value=0.01,
            optimal_lag=2,
            is_causal=True
        )
        
        assert result.f_statistic == 5.0
        assert result.p_value == 0.01
        assert result.optimal_lag == 2
        assert result.is_causal is True
    
    def test_granger_on_causal_data(self, validator, date_range):
        """Test Granger causality on data with causal relationship."""
        np.random.seed(42)
        n = len(date_range)
        
        # Create x that causes y with lag
        x = pd.Series(np.random.randn(n), index=date_range)
        y = pd.Series(
            0.5 * x.shift(1).fillna(0) + 0.3 * x.shift(2).fillna(0) + np.random.randn(n) * 0.3,
            index=date_range
        )
        
        result = validator._granger_causality(x, y)
        
        assert isinstance(result, GrangerResult)


class TestVixSpikePrediction(TestHypothesisValidator):
    """Tests for VIX spike prediction metrics."""

    def test_vix_spike_hit_rate_is_bounded(self, validator):
        """Hit rate should always be in [0, 1]."""
        idx = pd.date_range(start="2024-01-01", periods=15, freq="D")

        # Two strong drops before one spike.
        sentiment = pd.Series(
            [0, 0, 0, 0, -2, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4],
            index=idx,
            dtype=float,
        )
        vix = pd.Series([10, 10, 10, 10, 10, 10, 10, 10, 30, 10, 10, 10, 10, 10, 10], index=idx, dtype=float)

        hit_rate, fpr, avg_lead = validator._vix_spike_prediction(
            sentiment, vix, threshold=25.0, lead_window=5
        )

        assert 0.0 <= hit_rate <= 1.0
        assert 0.0 <= fpr <= 1.0
        assert avg_lead >= 0

    def test_vix_spike_counts_each_spike_once(self, validator):
        """Multiple drop signals should not count the same spike more than once."""
        idx = pd.date_range(start="2024-01-01", periods=15, freq="D")

        # Drops on Jan 5 and Jan 6, one spike on Jan 9.
        sentiment = pd.Series(
            [0, 0, 0, 0, -2, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4],
            index=idx,
            dtype=float,
        )
        vix = pd.Series([10, 10, 10, 10, 10, 10, 10, 10, 30, 10, 10, 10, 10, 10, 10], index=idx, dtype=float)

        hit_rate, fpr, _ = validator._vix_spike_prediction(
            sentiment, vix, threshold=25.0, lead_window=5
        )

        assert hit_rate == pytest.approx(1.0)
        assert fpr == pytest.approx(0.5)


class TestValidateAll(TestHypothesisValidator):
    """Tests for running all validations together."""
    
    def test_validate_all_returns_dict(
        self, 
        validator, 
        synthetic_sentiment_leading_vix,
        synthetic_divergence_before_transition,
        synthetic_connectedness_data
    ):
        """Test that validate_all returns proper dictionary."""
        sentiment, vix = synthetic_sentiment_leading_vix
        sentiment_by_asset, regime_series = synthetic_divergence_before_transition
        tci_series, regime_series2, crash_dates = synthetic_connectedness_data
        
        results = validator.validate_all(
            sentiment_series=sentiment,
            sentiment_by_asset=sentiment_by_asset,
            vix_series=vix,
            tci_series=tci_series,
            regime_series=regime_series,
            crash_dates=crash_dates
        )
        
        assert isinstance(results, dict)
        assert 'H1' in results
        assert 'H2' in results
        assert 'H3' in results


class TestReportGeneration(TestHypothesisValidator):
    """Tests for hypothesis report generation."""
    
    def test_generate_report(
        self,
        validator,
        synthetic_sentiment_leading_vix,
        synthetic_divergence_before_transition,
        synthetic_connectedness_data
    ):
        """Test report generation."""
        sentiment, vix = synthetic_sentiment_leading_vix
        sentiment_by_asset, regime_series = synthetic_divergence_before_transition
        tci_series, regime_series2, crash_dates = synthetic_connectedness_data
        
        results = validator.validate_all(
            sentiment_series=sentiment,
            sentiment_by_asset=sentiment_by_asset,
            vix_series=vix,
            tci_series=tci_series,
            regime_series=regime_series,
            crash_dates=crash_dates
        )
        
        report = generate_hypothesis_report(results)
        
        assert "HYPOTHESIS VALIDATION REPORT" in report
        assert "H1" in report
        assert "H2" in report
        assert "H3" in report
        assert "SUMMARY" in report
    
    def test_report_includes_summary_counts(
        self,
        validator,
        synthetic_sentiment_leading_vix,
        synthetic_divergence_before_transition,
        synthetic_connectedness_data
    ):
        """Test that report includes summary counts."""
        sentiment, vix = synthetic_sentiment_leading_vix
        sentiment_by_asset, regime_series = synthetic_divergence_before_transition
        tci_series, regime_series2, crash_dates = synthetic_connectedness_data
        
        results = validator.validate_all(
            sentiment_series=sentiment,
            sentiment_by_asset=sentiment_by_asset,
            vix_series=vix,
            tci_series=tci_series,
            regime_series=regime_series,
            crash_dates=crash_dates
        )
        
        report = generate_hypothesis_report(results)
        
        assert "Supported:" in report
        assert "Inconclusive:" in report
        assert "Not Supported:" in report


class TestHypothesisResultEnum:
    """Tests for HypothesisResult enum."""
    
    def test_hypothesis_result_values(self):
        """Test HypothesisResult enum values."""
        assert HypothesisResult.SUPPORTED.value == "supported"
        assert HypothesisResult.NOT_SUPPORTED.value == "not_supported"
        assert HypothesisResult.INCONCLUSIVE.value == "inconclusive"
    
    def test_hypothesis_result_is_string(self):
        """Test HypothesisResult is string enum."""
        assert isinstance(HypothesisResult.SUPPORTED.value, str)


class TestEdgeCases:
    """Tests for edge cases and error handling."""
    
    @pytest.fixture
    def validator(self):
        return HypothesisValidator()
    
    def test_empty_series(self, validator):
        """Test handling of empty series."""
        dates = pd.date_range(start='2020-01-01', periods=0, freq='D')
        sentiment = pd.Series([], index=dates, dtype=float)
        vix = pd.Series([], index=dates, dtype=float)
        
        result = validator.validate_h1(sentiment, vix)
        
        assert result.result == HypothesisResult.INCONCLUSIVE
    
    def test_misaligned_indices(self, validator):
        """Test handling of misaligned time series."""
        dates1 = pd.date_range(start='2020-01-01', periods=100, freq='D')
        dates2 = pd.date_range(start='2020-06-01', periods=100, freq='D')
        
        sentiment = pd.Series(np.random.randn(100), index=dates1)
        vix = pd.Series(np.random.randn(100) * 5 + 20, index=dates2)
        
        # Should handle non-overlapping indices gracefully
        result = validator.validate_h1(sentiment, vix)
        
        assert isinstance(result, H1Result)
    
    def test_constant_series(self, validator):
        """Test handling of constant series (zero variance)."""
        dates = pd.date_range(start='2020-01-01', periods=100, freq='D')
        sentiment = pd.Series(np.ones(100) * 0.5, index=dates)
        vix = pd.Series(np.ones(100) * 20, index=dates)
        
        # Should not crash on zero variance
        result = validator.validate_h1(sentiment, vix)
        
        assert isinstance(result, H1Result)
    
    def test_nan_handling(self, validator):
        """Test handling of NaN values."""
        dates = pd.date_range(start='2020-01-01', periods=100, freq='D')
        sentiment = pd.Series(np.random.randn(100), index=dates)
        vix = pd.Series(np.random.randn(100) * 5 + 20, index=dates)
        
        # Add some NaNs
        sentiment.iloc[10:15] = np.nan
        vix.iloc[50:55] = np.nan
        
        result = validator.validate_h1(sentiment.dropna(), vix.dropna())
        
        assert isinstance(result, H1Result)
