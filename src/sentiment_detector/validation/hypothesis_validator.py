"""
Hypothesis Validation Framework.

This module implements statistical tests for validating the research hypotheses:
- H1 (Leading Indicator): Sentiment leads VIX by 1-5 trading days
- H2 (Divergence Signal): Cross-asset sentiment divergence precedes regime transitions
- H3 (Network Effect): High connectedness correlates with regime stability

References:
- Bollen et al. (2011): 2-6 day predictive lead time
- Caferra (2022): Sentiment-mediated cross-market connections
- Cao et al. (2025): Entropy-based connectedness measures
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple, Literal
from enum import Enum
import logging
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from scipy import stats
from scipy.signal import correlate

logger = logging.getLogger(__name__)


class HypothesisResult(str, Enum):
    """Hypothesis test result."""
    SUPPORTED = "supported"
    NOT_SUPPORTED = "not_supported"
    INCONCLUSIVE = "inconclusive"


@dataclass
class LeadLagResult:
    """Result from lead-lag analysis."""
    optimal_lag: int  # Positive = sentiment leads
    max_correlation: float
    correlations_by_lag: Dict[int, float]
    p_value: float
    is_significant: bool
    confidence_interval: Tuple[float, float]


@dataclass
class GrangerResult:
    """Result from Granger causality test."""
    f_statistic: float
    p_value: float
    optimal_lag: int
    is_causal: bool  # At α = 0.05


@dataclass
class H1Result:
    """
    H1 (Leading Indicator Hypothesis) validation result.
    
    Tests: Cross-asset sentiment leads VIX by 1-5 days
    """
    hypothesis: str = "H1 (Leading Indicator)"
    result: HypothesisResult = HypothesisResult.INCONCLUSIVE
    
    # Lead-lag analysis
    lead_lag: Optional[LeadLagResult] = None
    
    # Granger causality
    granger: Optional[GrangerResult] = None
    
    # Summary statistics
    avg_lead_days: Optional[float] = None
    hit_rate: Optional[float] = None  # % of VIX spikes predicted
    false_positive_rate: Optional[float] = None
    
    # Evidence
    evidence: List[str] = field(default_factory=list)
    
    def summary(self) -> str:
        lines = [
            f"=== {self.hypothesis} ===",
            f"Result: {self.result.value.upper()}",
            f"",
        ]
        if self.lead_lag:
            lines.extend([
                f"Lead-Lag Analysis:",
                f"  Optimal lag: {self.lead_lag.optimal_lag} days (sentiment leads)",
                f"  Max correlation: {self.lead_lag.max_correlation:.4f}",
                f"  P-value: {self.lead_lag.p_value:.4f}",
                f"  Significant: {self.lead_lag.is_significant}",
            ])
        if self.granger:
            lines.extend([
                f"",
                f"Granger Causality:",
                f"  F-statistic: {self.granger.f_statistic:.4f}",
                f"  P-value: {self.granger.p_value:.4f}",
                f"  Sentiment Granger-causes VIX: {self.granger.is_causal}",
            ])
        if self.evidence:
            lines.extend(["", "Evidence:"] + [f"  - {e}" for e in self.evidence])
        return "\n".join(lines)


@dataclass
class H2Result:
    """
    H2 (Divergence Signal Hypothesis) validation result.
    
    Tests: Cross-asset sentiment divergence signals regime transitions
    """
    hypothesis: str = "H2 (Divergence Signal)"
    result: HypothesisResult = HypothesisResult.INCONCLUSIVE
    
    # Divergence metrics
    pre_transition_divergence: Optional[float] = None
    stable_period_divergence: Optional[float] = None
    divergence_ratio: Optional[float] = None  # pre/stable
    
    # Statistical test
    t_statistic: Optional[float] = None
    p_value: Optional[float] = None
    effect_size: Optional[float] = None  # Cohen's d
    
    # Prediction accuracy
    transition_detection_rate: Optional[float] = None
    avg_warning_days: Optional[float] = None
    
    evidence: List[str] = field(default_factory=list)
    
    def summary(self) -> str:
        lines = [
            f"=== {self.hypothesis} ===",
            f"Result: {self.result.value.upper()}",
        ]
        if self.divergence_ratio:
            lines.extend([
                f"",
                f"Divergence Analysis:",
                f"  Pre-transition divergence: {self.pre_transition_divergence:.4f}",
                f"  Stable period divergence: {self.stable_period_divergence:.4f}",
                f"  Ratio (pre/stable): {self.divergence_ratio:.2f}x",
            ])
        if self.p_value is not None:
            lines.extend([
                f"",
                f"Statistical Test (t-test):",
                f"  t-statistic: {self.t_statistic:.4f}",
                f"  P-value: {self.p_value:.4f}",
                f"  Effect size (Cohen's d): {self.effect_size:.4f}",
            ])
        if self.evidence:
            lines.extend(["", "Evidence:"] + [f"  - {e}" for e in self.evidence])
        return "\n".join(lines)


@dataclass
class H3Result:
    """
    H3 (Network Effect Hypothesis) validation result.
    
    Tests: High connectedness during stable regimes, disconnection before transitions
    """
    hypothesis: str = "H3 (Network Effect)"
    result: HypothesisResult = HypothesisResult.INCONCLUSIVE
    
    # Connectedness by regime
    stable_regime_tci: Optional[float] = None  # Total Connectedness Index
    transition_tci: Optional[float] = None
    pre_crash_tci_change: Optional[float] = None  # Rate of change before crash
    
    # Statistical test
    anova_f: Optional[float] = None
    anova_p: Optional[float] = None
    
    # Correlation with regime probability
    tci_regime_correlation: Optional[float] = None
    
    evidence: List[str] = field(default_factory=list)
    
    def summary(self) -> str:
        lines = [
            f"=== {self.hypothesis} ===",
            f"Result: {self.result.value.upper()}",
        ]
        if self.stable_regime_tci is not None:
            lines.extend([
                f"",
                f"Connectedness by Regime:",
                f"  Stable regime TCI: {self.stable_regime_tci:.4f}",
                f"  Transition period TCI: {self.transition_tci:.4f}" if self.transition_tci is not None else "  Transition period TCI: N/A",
            ])
            if self.pre_crash_tci_change is not None:
                lines.append(f"  Pre-crash TCI change rate: {self.pre_crash_tci_change:.4f}")
        if self.anova_p is not None:
            lines.extend([
                f"",
                f"ANOVA Test (TCI across regimes):",
                f"  F-statistic: {self.anova_f:.4f}",
                f"  P-value: {self.anova_p:.4f}",
            ])
        if self.evidence:
            lines.extend(["", "Evidence:"] + [f"  - {e}" for e in self.evidence])
        return "\n".join(lines)


class HypothesisValidator:
    """
    Framework for validating research hypotheses H1, H2, H3.
    
    Example:
        >>> validator = HypothesisValidator()
        >>> h1_result = validator.validate_h1(
        ...     sentiment_series=sentiment_df['compound'],
        ...     vix_series=vix_df['close'],
        ...     regime_series=regime_df['regime']
        ... )
        >>> print(h1_result.summary())
    """
    
    def __init__(
        self,
        significance_level: float = 0.05,
        max_lag_days: int = 10,
        min_effect_size: float = 0.3  # Cohen's d threshold
    ):
        """
        Initialize hypothesis validator.
        
        Args:
            significance_level: Alpha for statistical tests
            max_lag_days: Maximum lag to test for lead-lag analysis
            min_effect_size: Minimum Cohen's d for practical significance
        """
        self.alpha = significance_level
        self.max_lag = max_lag_days
        self.min_effect_size = min_effect_size
        
        logger.info(f"HypothesisValidator initialized: α={self.alpha}, max_lag={self.max_lag}")
    
    def validate_h1(
        self,
        sentiment_series: pd.Series,
        vix_series: pd.Series,
        regime_series: Optional[pd.Series] = None,
        vix_spike_threshold: float = 25.0
    ) -> H1Result:
        """
        Validate H1: Cross-asset sentiment leads VIX by 1-5 trading days.
        
        Tests:
        1. Lead-lag cross-correlation analysis
        2. Granger causality test
        3. VIX spike prediction accuracy
        
        Args:
            sentiment_series: Daily aggregate sentiment scores
            vix_series: Daily VIX closing values
            regime_series: Optional regime labels for context
            vix_spike_threshold: VIX level considered "spike"
        
        Returns:
            H1Result with statistical evidence
        """
        result = H1Result()
        
        # Align series
        sentiment, vix = self._align_series(sentiment_series, vix_series)
        
        if len(sentiment) < 30:
            result.evidence.append(f"Insufficient data: only {len(sentiment)} observations")
            return result
        
        # 1. Lead-lag cross-correlation
        lead_lag = self._compute_lead_lag(sentiment.values, vix.values)
        result.lead_lag = lead_lag
        
        # 2. Granger causality
        granger = self._granger_causality(sentiment, vix)
        result.granger = granger
        
        # 3. VIX spike prediction
        if vix_spike_threshold:
            hit_rate, fpr, avg_lead = self._vix_spike_prediction(
                sentiment, vix, threshold=vix_spike_threshold
            )
            result.hit_rate = hit_rate
            result.false_positive_rate = fpr
            result.avg_lead_days = avg_lead
        
        # Determine overall result
        evidence_count = 0
        
        if lead_lag.is_significant and 1 <= lead_lag.optimal_lag <= 5:
            evidence_count += 1
            result.evidence.append(
                f"Lead-lag: Sentiment leads VIX by {lead_lag.optimal_lag} days (r={lead_lag.max_correlation:.3f}, p<{self.alpha})"
            )
        
        if granger.is_causal:
            evidence_count += 1
            result.evidence.append(
                f"Granger: Sentiment Granger-causes VIX (F={granger.f_statistic:.2f}, p={granger.p_value:.4f})"
            )
        
        if result.hit_rate and result.hit_rate > 0.6:
            evidence_count += 1
            result.evidence.append(
                f"VIX spikes: {result.hit_rate:.1%} detected with avg {result.avg_lead_days:.1f} days warning"
            )
        
        # Verdict
        if evidence_count >= 2:
            result.result = HypothesisResult.SUPPORTED
        elif evidence_count == 1:
            result.result = HypothesisResult.INCONCLUSIVE
        else:
            result.result = HypothesisResult.NOT_SUPPORTED
        
        return result
    
    def validate_h2(
        self,
        sentiment_by_asset: pd.DataFrame,
        regime_series: pd.Series,
        transition_window_days: int = 5
    ) -> H2Result:
        """
        Validate H2: Cross-asset sentiment divergence signals regime transitions.
        
        Tests:
        1. Compare divergence in pre-transition vs. stable periods
        2. T-test for significance
        3. Effect size (Cohen's d)
        
        Args:
            sentiment_by_asset: DataFrame with columns for each asset class sentiment
            regime_series: Regime labels (risk_on, risk_off, transition)
            transition_window_days: Days before transition to analyze
        
        Returns:
            H2Result with statistical evidence
        """
        result = H2Result()
        
        # Align data
        common_idx = sentiment_by_asset.index.intersection(regime_series.index)
        sentiment = sentiment_by_asset.loc[common_idx]
        regimes = regime_series.loc[common_idx]
        
        if len(common_idx) < 30:
            result.evidence.append(f"Insufficient data: only {len(common_idx)} observations")
            return result
        
        # Calculate divergence (std across asset classes)
        divergence = sentiment.std(axis=1)
        
        # Identify transition points
        regime_changes = regimes != regimes.shift(1)
        transition_points = regime_changes[regime_changes].index
        
        if len(transition_points) < 3:
            result.evidence.append(f"Insufficient transitions: only {len(transition_points)}")
            return result
        
        # Get pre-transition divergence (window before each transition)
        pre_transition_divs = []
        for tp in transition_points:
            start = tp - timedelta(days=transition_window_days)
            pre_window = divergence[(divergence.index >= start) & (divergence.index < tp)]
            if len(pre_window) > 0:
                pre_transition_divs.extend(pre_window.values)
        
        # Get stable period divergence (periods without transitions)
        stable_mask = ~regime_changes
        stable_divs = divergence[stable_mask].values
        
        if len(pre_transition_divs) < 5 or len(stable_divs) < 10:
            result.evidence.append("Insufficient data in comparison windows")
            return result
        
        pre_transition_divs = np.array(pre_transition_divs)
        
        # Statistical comparison
        result.pre_transition_divergence = np.mean(pre_transition_divs)
        result.stable_period_divergence = np.mean(stable_divs)
        result.divergence_ratio = result.pre_transition_divergence / result.stable_period_divergence
        
        # T-test
        t_stat, p_val = stats.ttest_ind(pre_transition_divs, stable_divs)
        result.t_statistic = float(t_stat)
        result.p_value = float(p_val)
        
        # Effect size (Cohen's d)
        pooled_std = np.sqrt(
            (np.var(pre_transition_divs) + np.var(stable_divs)) / 2
        )
        result.effect_size = (result.pre_transition_divergence - result.stable_period_divergence) / pooled_std
        
        # Build evidence
        if result.divergence_ratio > 1.2:
            result.evidence.append(
                f"Pre-transition divergence {result.divergence_ratio:.1f}x higher than stable periods"
            )
        
        if result.p_value < self.alpha:
            result.evidence.append(
                f"Difference is statistically significant (p={result.p_value:.4f})"
            )
        
        if abs(result.effect_size) >= self.min_effect_size:
            result.evidence.append(
                f"Practically significant effect (Cohen's d={result.effect_size:.2f})"
            )
        
        # Verdict
        if result.p_value < self.alpha and abs(result.effect_size) >= self.min_effect_size:
            result.result = HypothesisResult.SUPPORTED
        elif result.p_value < self.alpha or result.divergence_ratio > 1.5:
            result.result = HypothesisResult.INCONCLUSIVE
        else:
            result.result = HypothesisResult.NOT_SUPPORTED
        
        return result
    
    def validate_h3(
        self,
        tci_series: pd.Series,
        regime_series: pd.Series,
        crash_dates: Optional[List[datetime]] = None
    ) -> H3Result:
        """
        Validate H3: High connectedness during stable regimes, disconnection before transitions.
        
        Tests:
        1. ANOVA comparing TCI across regime states
        2. TCI rate of change before crash events
        3. Correlation between TCI and regime stability
        
        Args:
            tci_series: Total Connectedness Index over time
            regime_series: Regime labels
            crash_dates: Known crash event dates for targeted analysis
        
        Returns:
            H3Result with statistical evidence
        """
        result = H3Result()
        
        # Align data
        common_idx = tci_series.index.intersection(regime_series.index)
        tci = tci_series.loc[common_idx]
        regimes = regime_series.loc[common_idx]
        
        if len(common_idx) < 30:
            result.evidence.append(f"Insufficient data: only {len(common_idx)} observations")
            return result
        
        # Group TCI by regime
        regime_groups = {}
        for regime in regimes.unique():
            regime_groups[regime] = tci[regimes == regime].values
        
        # Calculate TCI by regime type
        stable_regimes = ['risk_on', 'low_volatility', 'normal', 'stable']
        transition_regimes = ['transition', 'risk_off', 'elevated', 'high_volatility', 'crash']
        
        stable_tci = []
        transition_tci = []
        
        for regime, values in regime_groups.items():
            regime_lower = str(regime).lower()
            if any(s in regime_lower for s in ['risk_on', 'low', 'normal', 'stable']):
                stable_tci.extend(values)
            elif any(s in regime_lower for s in ['transition', 'risk_off', 'elevated', 'high', 'crash']):
                transition_tci.extend(values)
            else:
                # Unknown regime - add to stable by default
                stable_tci.extend(values)
        
        if len(stable_tci) < 5 or len(transition_tci) < 5:
            result.evidence.append("Insufficient data for regime comparison")
            return result
        
        result.stable_regime_tci = np.mean(stable_tci)
        result.transition_tci = np.mean(transition_tci)
        
        # ANOVA across all regime groups
        groups = [v for v in regime_groups.values() if len(v) >= 5]
        if len(groups) >= 2:
            f_stat, p_val = stats.f_oneway(*groups)
            result.anova_f = float(f_stat)
            result.anova_p = float(p_val)
        
        # Pre-crash TCI analysis
        if crash_dates:
            pre_crash_changes = []
            for crash_date in crash_dates:
                try:
                    crash_dt = pd.Timestamp(crash_date)
                    pre_crash = tci[(tci.index >= crash_dt - timedelta(days=10)) & 
                                   (tci.index < crash_dt)]
                    if len(pre_crash) >= 3:
                        # Calculate rate of change
                        change_rate = (pre_crash.iloc[-1] - pre_crash.iloc[0]) / len(pre_crash)
                        pre_crash_changes.append(change_rate)
                except:
                    continue
            
            if pre_crash_changes:
                result.pre_crash_tci_change = np.mean(pre_crash_changes)
        
        # Build evidence
        if result.stable_regime_tci > result.transition_tci:
            result.evidence.append(
                f"TCI higher in stable regimes ({result.stable_regime_tci:.3f}) vs transitions ({result.transition_tci:.3f})"
            )
        
        if result.anova_p and result.anova_p < self.alpha:
            result.evidence.append(
                f"Significant TCI difference across regimes (ANOVA p={result.anova_p:.4f})"
            )
        
        if result.pre_crash_tci_change and result.pre_crash_tci_change < 0:
            result.evidence.append(
                f"TCI decreases before crashes (avg change: {result.pre_crash_tci_change:.4f})"
            )
        
        # Verdict
        evidence_count = len(result.evidence)
        if evidence_count >= 2:
            result.result = HypothesisResult.SUPPORTED
        elif evidence_count == 1:
            result.result = HypothesisResult.INCONCLUSIVE
        else:
            result.result = HypothesisResult.NOT_SUPPORTED
        
        return result
    
    def validate_all(
        self,
        sentiment_series: pd.Series,
        sentiment_by_asset: pd.DataFrame,
        vix_series: pd.Series,
        tci_series: pd.Series,
        regime_series: pd.Series,
        crash_dates: Optional[List[datetime]] = None
    ) -> Dict[str, object]:
        """
        Run all hypothesis validations.
        
        Returns:
            Dictionary with H1, H2, H3 results
        """
        results = {}
        
        logger.info("Validating H1 (Leading Indicator)...")
        results['H1'] = self.validate_h1(sentiment_series, vix_series, regime_series)
        
        logger.info("Validating H2 (Divergence Signal)...")
        results['H2'] = self.validate_h2(sentiment_by_asset, regime_series)
        
        logger.info("Validating H3 (Network Effect)...")
        results['H3'] = self.validate_h3(tci_series, regime_series, crash_dates)
        
        return results
    
    def _align_series(
        self, 
        s1: pd.Series, 
        s2: pd.Series
    ) -> Tuple[pd.Series, pd.Series]:
        """Align two series to common index."""
        common_idx = s1.index.intersection(s2.index)
        return s1.loc[common_idx], s2.loc[common_idx]
    
    def _compute_lead_lag(
        self, 
        x: np.ndarray, 
        y: np.ndarray
    ) -> LeadLagResult:
        """
        Compute lead-lag relationship via cross-correlation.
        
        Positive lag means x leads y.
        """
        # Normalize
        x = (x - np.mean(x)) / (np.std(x) + 1e-8)
        y = (y - np.mean(y)) / (np.std(y) + 1e-8)
        
        # Cross-correlation
        correlations = {}
        for lag in range(-self.max_lag, self.max_lag + 1):
            if lag > 0:
                # x leads y
                corr = np.corrcoef(x[:-lag], y[lag:])[0, 1]
            elif lag < 0:
                # y leads x
                corr = np.corrcoef(x[-lag:], y[:lag])[0, 1]
            else:
                corr = np.corrcoef(x, y)[0, 1]
            correlations[lag] = corr if not np.isnan(corr) else 0
        
        # Find optimal lag
        optimal_lag = max(correlations, key=lambda k: abs(correlations[k]))
        max_corr = correlations[optimal_lag]
        
        # Statistical significance (Fisher transformation)
        n = len(x) - abs(optimal_lag)
        z = 0.5 * np.log((1 + max_corr) / (1 - max_corr + 1e-8))
        se = 1 / np.sqrt(n - 3) if n > 3 else float('inf')
        z_stat = z / se
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
        
        # Confidence interval
        z_crit = stats.norm.ppf(1 - self.alpha / 2)
        ci_low = np.tanh(z - z_crit * se)
        ci_high = np.tanh(z + z_crit * se)
        
        return LeadLagResult(
            optimal_lag=optimal_lag,
            max_correlation=max_corr,
            correlations_by_lag=correlations,
            p_value=p_value,
            is_significant=p_value < self.alpha,
            confidence_interval=(ci_low, ci_high)
        )
    
    def _granger_causality(
        self, 
        x: pd.Series, 
        y: pd.Series, 
        max_lag: int = 5
    ) -> GrangerResult:
        """
        Test if x Granger-causes y.
        
        Uses statsmodels if available, otherwise simple F-test.
        """
        try:
            from statsmodels.tsa.stattools import grangercausalitytests
            
            data = pd.DataFrame({'x': x.values, 'y': y.values}).dropna()
            
            if len(data) < max_lag * 3:
                return GrangerResult(0, 1.0, 1, False)
            
            # Run Granger test
            results = grangercausalitytests(data[['y', 'x']], maxlag=max_lag, verbose=False)
            
            # Find best lag by F-test p-value
            best_lag = 1
            best_p = 1.0
            best_f = 0
            
            for lag, result in results.items():
                f_test = result[0]['ssr_ftest']
                if f_test[1] < best_p:
                    best_p = f_test[1]
                    best_f = f_test[0]
                    best_lag = lag
            
            return GrangerResult(
                f_statistic=float(best_f),
                p_value=float(best_p),
                optimal_lag=best_lag,
                is_causal=best_p < self.alpha
            )
            
        except ImportError:
            logger.warning("statsmodels not available, using simple correlation test")
            return GrangerResult(0, 1.0, 1, False)
    
    def _vix_spike_prediction(
        self,
        sentiment: pd.Series,
        vix: pd.Series,
        threshold: float = 25.0,
        lead_window: int = 5
    ) -> Tuple[float, float, float]:
        """
        Calculate VIX spike prediction accuracy.
        
        Returns:
            Tuple of (hit_rate, false_positive_rate, avg_lead_days)
        """
        # Identify VIX spikes
        vix_spikes = vix > threshold
        spike_dates = vix_spikes[vix_spikes].index
        
        if len(spike_dates) == 0:
            return 0, 0, 0
        
        # Identify sentiment drops (potential warning signals)
        sentiment_drop = sentiment.diff() < -sentiment.std()
        
        hits = 0
        false_positives = 0
        lead_times = []
        
        for drop_date in sentiment.index[sentiment_drop]:
            # Check if VIX spike occurs within lead_window days
            future_window = [drop_date + timedelta(days=i) for i in range(1, lead_window + 1)]
            
            spike_found = False
            for i, future_date in enumerate(future_window):
                if future_date in spike_dates:
                    hits += 1
                    lead_times.append(i + 1)
                    spike_found = True
                    break
            
            if not spike_found:
                false_positives += 1
        
        total_signals = hits + false_positives
        hit_rate = hits / len(spike_dates) if len(spike_dates) > 0 else 0
        fpr = false_positives / total_signals if total_signals > 0 else 0
        avg_lead = np.mean(lead_times) if lead_times else 0
        
        return hit_rate, fpr, avg_lead


def generate_hypothesis_report(
    results: Dict[str, object],
    output_path: Optional[str] = None
) -> str:
    """
    Generate a formatted hypothesis validation report.
    
    Args:
        results: Dictionary with H1, H2, H3 results
        output_path: Optional path to save report
    
    Returns:
        Formatted report string
    """
    lines = [
        "=" * 60,
        "HYPOTHESIS VALIDATION REPORT",
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "=" * 60,
        "",
    ]
    
    for key in ['H1', 'H2', 'H3']:
        if key in results:
            lines.append(results[key].summary())
            lines.append("")
            lines.append("-" * 60)
            lines.append("")
    
    # Summary
    supported = sum(1 for r in results.values() if r.result == HypothesisResult.SUPPORTED)
    inconclusive = sum(1 for r in results.values() if r.result == HypothesisResult.INCONCLUSIVE)
    not_supported = sum(1 for r in results.values() if r.result == HypothesisResult.NOT_SUPPORTED)
    
    lines.extend([
        "SUMMARY",
        "=" * 60,
        f"Supported: {supported}/3",
        f"Inconclusive: {inconclusive}/3",
        f"Not Supported: {not_supported}/3",
    ])
    
    report = "\n".join(lines)
    
    if output_path:
        with open(output_path, 'w') as f:
            f.write(report)
        logger.info(f"Report saved to {output_path}")
    
    return report
