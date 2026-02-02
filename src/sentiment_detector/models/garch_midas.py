"""
GARCH-MIDAS Model for Volatility with Sentiment.

This module implements the GARCH-MIDAS (Mixed Data Sampling) model
that incorporates sentiment indices as exogenous variables for
volatility forecasting.

Per Dakalbab et al. (2024), GARCH-MIDAS serves as Layer 1 of the
regime detection framework, providing volatility estimates that
feed into the Statistical Jump Model (Layer 2).

Key Features:
- GARCH(1,1) for short-term volatility dynamics
- MIDAS weighting for low-frequency sentiment data
- Beta polynomial weighting function
- Forecast horizon flexibility

References:
- Engle, R.F. et al. (2013) "Stock Market Volatility and Macroeconomic Fundamentals"
- Dakalbab, F. et al. (2024) Sentiment-based regime detection
"""

from dataclasses import dataclass, field
from typing import Optional, Literal, Union
import logging
import warnings

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# Try to import arch library
try:
    from arch import arch_model
    from arch.univariate import GARCH, ConstantMean, Normal
    ARCH_AVAILABLE = True
except ImportError:
    ARCH_AVAILABLE = False
    logger.warning("arch library not available. GARCH-MIDAS will use fallback.")


@dataclass
class MIDASWeights:
    """
    MIDAS weighting scheme using Beta polynomial.
    
    The Beta polynomial provides flexible weighting of
    low-frequency variables (e.g., monthly sentiment)
    when combined with high-frequency data (e.g., daily returns).
    
    Attributes:
        omega1: First shape parameter (default 1.0)
        omega2: Second shape parameter (controls decay)
        K: Number of lags in MIDAS polynomial
        weights: Computed weights array
    """
    omega1: float = 1.0
    omega2: float = 1.0
    K: int = 22  # Approximately one month of trading days
    weights: np.ndarray = field(default_factory=lambda: np.array([]))
    
    def __post_init__(self):
        """Compute weights after initialization."""
        self.weights = self.compute_weights()
    
    def compute_weights(self) -> np.ndarray:
        """
        Compute Beta polynomial weights.
        
        w_k = (k/K)^(omega1-1) * (1 - k/K)^(omega2-1) / sum(weights)
        
        Returns:
            Normalized weight array of length K
        """
        k = np.arange(1, self.K + 1)
        x = k / self.K
        
        # Beta polynomial
        raw_weights = np.power(x, self.omega1 - 1) * np.power(1 - x, self.omega2 - 1)
        
        # Handle numerical issues
        raw_weights = np.nan_to_num(raw_weights, nan=0.0)
        
        # Normalize
        total = np.sum(raw_weights)
        if total > 0:
            return raw_weights / total
        else:
            return np.ones(self.K) / self.K


@dataclass
class GARCHMIDASResult:
    """
    Result from GARCH-MIDAS model estimation.
    
    Attributes:
        conditional_volatility: Time series of estimated volatility
        long_run_volatility: MIDAS component (slow-moving)
        short_run_volatility: GARCH component (fast-moving)
        params: Estimated parameters
        sentiment_coefficient: Coefficient on sentiment variable
        aic: Akaike Information Criterion
        bic: Bayesian Information Criterion
        log_likelihood: Log likelihood value
        residuals: Standardized residuals
        midas_weights: Weights used for MIDAS component
    """
    conditional_volatility: pd.Series
    long_run_volatility: pd.Series
    short_run_volatility: pd.Series
    params: dict[str, float]
    sentiment_coefficient: Optional[float]
    aic: float
    bic: float
    log_likelihood: float
    residuals: pd.Series
    midas_weights: MIDASWeights
    convergence: bool = True
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "params": self.params,
            "sentiment_coefficient": self.sentiment_coefficient,
            "aic": self.aic,
            "bic": self.bic,
            "log_likelihood": self.log_likelihood,
            "convergence": self.convergence,
            "midas_K": self.midas_weights.K,
            "volatility_stats": {
                "mean": float(self.conditional_volatility.mean()),
                "std": float(self.conditional_volatility.std()),
                "min": float(self.conditional_volatility.min()),
                "max": float(self.conditional_volatility.max()),
            }
        }


class GARCHMIDASModel:
    """
    GARCH-MIDAS model with sentiment as exogenous variable.
    
    This model decomposes volatility into:
    1. Short-run component (GARCH) - daily dynamics
    2. Long-run component (MIDAS) - sentiment-driven
    
    The total conditional variance is:
        σ²_t = τ_t × g_t
        
    Where:
        - τ_t is the long-run (MIDAS) component
        - g_t is the short-run (GARCH) component
    
    Example:
        >>> model = GARCHMIDASModel(midas_lags=22)
        >>> result = model.fit(returns, sentiment_index)
        >>> forecast = model.forecast(steps=5)
    """
    
    def __init__(
        self,
        p: int = 1,
        q: int = 1,
        midas_lags: int = 22,
        midas_omega1: float = 1.0,
        midas_omega2: float = 1.0,
        distribution: Literal["normal", "t", "skewt"] = "normal"
    ):
        """
        Initialize GARCH-MIDAS model.
        
        Args:
            p: GARCH lag order (default 1)
            q: ARCH lag order (default 1)
            midas_lags: Number of lags for MIDAS component
            midas_omega1: Beta polynomial parameter 1
            midas_omega2: Beta polynomial parameter 2
            distribution: Error distribution assumption
        """
        self.p = p
        self.q = q
        self.midas_lags = midas_lags
        self.midas_weights = MIDASWeights(
            omega1=midas_omega1,
            omega2=midas_omega2,
            K=midas_lags
        )
        self.distribution = distribution
        
        self._fitted_model = None
        self._result = None
        self._returns = None
        self._sentiment = None
    
    def _compute_midas_component(
        self,
        sentiment: pd.Series,
        returns: pd.Series
    ) -> pd.Series:
        """
        Compute the MIDAS (long-run) volatility component.
        
        Uses weighted average of past sentiment to predict
        long-run volatility level.
        
        Args:
            sentiment: Sentiment index series
            returns: Returns series for alignment
            
        Returns:
            Long-run volatility component (tau)
        """
        # Align sentiment with returns
        aligned_sentiment = sentiment.reindex(returns.index, method='ffill')
        
        # Apply MIDAS weights to lagged sentiment
        tau = pd.Series(index=returns.index, dtype=float)
        weights = self.midas_weights.weights
        K = self.midas_lags
        
        for i, idx in enumerate(returns.index):
            if i < K:
                # Not enough history, use available data
                available = aligned_sentiment.iloc[:i+1].values
                if len(available) > 0:
                    w = weights[:len(available)]
                    w = w / w.sum()  # Renormalize
                    tau.loc[idx] = np.dot(w, available)
                else:
                    tau.loc[idx] = 0.0
            else:
                # Full history available
                lag_values = aligned_sentiment.iloc[i-K+1:i+1].values
                tau.loc[idx] = np.dot(weights, lag_values)
        
        # Transform to volatility scale (exponential link)
        # log(τ_t) = m + θ × weighted_sentiment
        tau_scaled = np.exp(tau)
        
        return tau_scaled
    
    def fit(
        self,
        returns: pd.Series,
        sentiment: Optional[pd.Series] = None,
        update_freq: int = 1,
        starting_values: Optional[dict] = None
    ) -> GARCHMIDASResult:
        """
        Fit GARCH-MIDAS model to data.
        
        Args:
            returns: Daily returns series (percentage)
            sentiment: Sentiment index series (aligned or daily)
            update_freq: Frequency of MIDAS component update
            starting_values: Optional starting values for optimization
            
        Returns:
            GARCHMIDASResult with fitted model outputs
        """
        if not ARCH_AVAILABLE:
            return self._fit_fallback(returns, sentiment)
        
        self._returns = returns.dropna()
        self._sentiment = sentiment
        
        # Compute MIDAS component if sentiment provided
        if sentiment is not None:
            tau = self._compute_midas_component(sentiment, self._returns)
            # Demean returns by long-run component
            adjusted_returns = self._returns / np.sqrt(tau)
        else:
            tau = pd.Series(1.0, index=self._returns.index)
            adjusted_returns = self._returns
        
        # Fit GARCH model to adjusted returns
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                
                model = arch_model(
                    adjusted_returns * 100,  # Convert to percentage
                    mean='Constant',
                    vol='GARCH',
                    p=self.p,
                    q=self.q,
                    dist=self.distribution
                )
                
                res = model.fit(disp='off', show_warning=False)
                
            # Extract results
            short_run_vol = res.conditional_volatility / 100
            long_run_vol = np.sqrt(tau)
            conditional_vol = short_run_vol * long_run_vol
            
            # Estimate sentiment coefficient from regression
            sentiment_coef = None
            if sentiment is not None:
                # Simple regression of log variance on sentiment
                log_var = np.log(res.conditional_volatility ** 2)
                aligned_sent = sentiment.reindex(log_var.index, method='ffill').fillna(0)
                
                # Use numpy for regression
                X = np.column_stack([np.ones(len(aligned_sent)), aligned_sent.values])
                y = log_var.values
                valid = ~(np.isnan(X).any(axis=1) | np.isnan(y))
                
                if valid.sum() > 10:
                    coefs = np.linalg.lstsq(X[valid], y[valid], rcond=None)[0]
                    sentiment_coef = float(coefs[1])
            
            self._result = GARCHMIDASResult(
                conditional_volatility=conditional_vol,
                long_run_volatility=pd.Series(long_run_vol, index=self._returns.index),
                short_run_volatility=short_run_vol,
                params={
                    "mu": float(res.params.get("mu", 0)),
                    "omega": float(res.params.get("omega", 0)),
                    "alpha": float(res.params.get("alpha[1]", 0)),
                    "beta": float(res.params.get("beta[1]", 0)),
                },
                sentiment_coefficient=sentiment_coef,
                aic=float(res.aic),
                bic=float(res.bic),
                log_likelihood=float(res.loglikelihood),
                residuals=res.resid / res.conditional_volatility,
                midas_weights=self.midas_weights,
                convergence=res.convergence_flag == 0
            )
            
            self._fitted_model = res
            
        except Exception as e:
            logger.error(f"GARCH-MIDAS fitting failed: {e}")
            return self._fit_fallback(returns, sentiment)
        
        return self._result
    
    def _fit_fallback(
        self,
        returns: pd.Series,
        sentiment: Optional[pd.Series] = None
    ) -> GARCHMIDASResult:
        """
        Fallback implementation using exponentially weighted variance.
        
        Used when arch library is not available or fitting fails.
        """
        logger.warning("Using fallback EWMA volatility estimation")
        
        returns = returns.dropna()
        
        # EWMA volatility as proxy
        lambda_param = 0.94  # RiskMetrics standard
        ewma_var = returns.ewm(alpha=1-lambda_param).var()
        short_run_vol = np.sqrt(ewma_var)
        
        # Simple sentiment scaling
        if sentiment is not None:
            tau = self._compute_midas_component(sentiment, returns)
            long_run_vol = np.sqrt(tau)
            conditional_vol = short_run_vol * long_run_vol
            
            # Simple correlation as coefficient proxy
            aligned_sent = sentiment.reindex(returns.index, method='ffill')
            sentiment_coef = float(np.corrcoef(
                short_run_vol.fillna(0).values,
                aligned_sent.fillna(0).values
            )[0, 1])
        else:
            long_run_vol = pd.Series(1.0, index=returns.index)
            conditional_vol = short_run_vol
            sentiment_coef = None
        
        return GARCHMIDASResult(
            conditional_volatility=conditional_vol,
            long_run_volatility=long_run_vol,
            short_run_volatility=short_run_vol,
            params={
                "mu": float(returns.mean()),
                "omega": float(returns.var()),
                "alpha": 0.05,
                "beta": 0.90,
            },
            sentiment_coefficient=sentiment_coef,
            aic=np.nan,
            bic=np.nan,
            log_likelihood=np.nan,
            residuals=returns / short_run_vol,
            midas_weights=self.midas_weights,
            convergence=True
        )
    
    def forecast(
        self,
        steps: int = 5,
        sentiment_forecast: Optional[pd.Series] = None
    ) -> pd.DataFrame:
        """
        Forecast volatility for future periods.
        
        Args:
            steps: Number of periods to forecast
            sentiment_forecast: Optional future sentiment values
            
        Returns:
            DataFrame with volatility forecasts and bounds
        """
        if self._result is None:
            raise ValueError("Model must be fitted before forecasting")
        
        if not ARCH_AVAILABLE or self._fitted_model is None:
            # Simple forecast using last values
            last_vol = self._result.conditional_volatility.iloc[-1]
            
            forecasts = pd.DataFrame({
                "mean": [last_vol] * steps,
                "lower": [last_vol * 0.8] * steps,
                "upper": [last_vol * 1.2] * steps
            })
            return forecasts
        
        # Use arch's forecast method
        try:
            fcast = self._fitted_model.forecast(horizon=steps)
            
            mean_forecast = np.sqrt(fcast.variance.iloc[-1].values) / 100
            
            # Adjust by long-run component if sentiment forecast provided
            if sentiment_forecast is not None and self._sentiment is not None:
                # Extend tau forecast
                tau_last = self._result.long_run_volatility.iloc[-1]
                tau_forecast = [tau_last] * steps
                mean_forecast = mean_forecast * np.sqrt(tau_forecast)
            
            forecasts = pd.DataFrame({
                "mean": mean_forecast,
                "lower": mean_forecast * 0.7,
                "upper": mean_forecast * 1.3
            })
            
            return forecasts
            
        except Exception as e:
            logger.error(f"Forecasting failed: {e}")
            last_vol = self._result.conditional_volatility.iloc[-1]
            return pd.DataFrame({
                "mean": [last_vol] * steps,
                "lower": [last_vol * 0.8] * steps,
                "upper": [last_vol * 1.2] * steps
            })
    
    def get_volatility_regimes(
        self,
        thresholds: Optional[tuple[float, float]] = None
    ) -> pd.Series:
        """
        Classify volatility into regime states.
        
        Args:
            thresholds: (low, high) quantile thresholds
                       Default (0.25, 0.75)
        
        Returns:
            Series with regime labels: 'low', 'normal', 'high'
        """
        if self._result is None:
            raise ValueError("Model must be fitted first")
        
        vol = self._result.conditional_volatility
        
        if thresholds is None:
            thresholds = (0.25, 0.75)
        
        low_thresh = vol.quantile(thresholds[0])
        high_thresh = vol.quantile(thresholds[1])
        
        regimes = pd.Series(index=vol.index, dtype=str)
        regimes[vol <= low_thresh] = 'low'
        regimes[(vol > low_thresh) & (vol <= high_thresh)] = 'normal'
        regimes[vol > high_thresh] = 'high'
        
        return regimes


def compute_sentiment_index(
    daily_sentiments: pd.DataFrame,
    aggregation: Literal["mean", "median", "net"] = "net"
) -> pd.Series:
    """
    Compute daily sentiment index from raw sentiment scores.
    
    Args:
        daily_sentiments: DataFrame with columns:
            - date: Date
            - sentiment: Score (-1 to 1) or label
            - confidence: Optional confidence weight
        aggregation: Method for aggregation
            - "mean": Simple average
            - "median": Median value
            - "net": (positive - negative) / total
            
    Returns:
        Daily sentiment index series
    """
    if 'date' not in daily_sentiments.columns:
        raise ValueError("DataFrame must have 'date' column")
    
    # Group by date
    grouped = daily_sentiments.groupby('date')
    
    if aggregation == "mean":
        index = grouped['sentiment'].mean()
    elif aggregation == "median":
        index = grouped['sentiment'].median()
    elif aggregation == "net":
        # Net sentiment: (positive - negative) / total
        def net_sentiment(group):
            pos = (group['sentiment'] > 0).sum()
            neg = (group['sentiment'] < 0).sum()
            total = len(group)
            return (pos - neg) / total if total > 0 else 0.0
        
        index = grouped.apply(net_sentiment)
    else:
        raise ValueError(f"Unknown aggregation: {aggregation}")
    
    return index


class GARCHMIDASWithCISS(GARCHMIDASModel):
    """
    Extended GARCH-MIDAS model with ECB CISS stress index integration.
    
    This model extends the base GARCH-MIDAS to incorporate:
    1. Sentiment index (social/news sentiment)
    2. ECB CISS (systemic stress indicator)
    
    The long-run volatility component τ_t is modeled as:
        log(τ_t) = m + θ_1 × sentiment_midas + θ_2 × ciss_midas
    
    Where:
    - sentiment_midas: MIDAS-weighted sentiment index
    - ciss_midas: MIDAS-weighted CISS values
    
    This allows the model to capture both:
    - Sentiment-driven volatility (retail/news sentiment)
    - Systemic stress (institutional/market-wide stress)
    
    Example:
        >>> model = GARCHMIDASWithCISS()
        >>> result = model.fit_with_ciss(
        ...     returns=spy_returns,
        ...     sentiment=sentiment_index,
        ...     ciss=ciss_series,
        ... )
    """
    
    def __init__(
        self,
        p: int = 1,
        q: int = 1,
        midas_lags: int = 22,
        midas_omega1: float = 1.0,
        midas_omega2: float = 1.0,
        distribution: Literal["normal", "t", "skewt"] = "t",
        ciss_weight: float = 0.5,
    ):
        """
        Initialize GARCH-MIDAS with CISS.
        
        Args:
            p, q: GARCH orders
            midas_lags: Number of lags for MIDAS weighting
            midas_omega1, midas_omega2: Beta polynomial parameters
            distribution: Error distribution
            ciss_weight: Weight for CISS vs sentiment in combined index
                         0 = sentiment only, 1 = CISS only
        """
        super().__init__(
            p=p, q=q, 
            midas_lags=midas_lags,
            midas_omega1=midas_omega1,
            midas_omega2=midas_omega2,
            distribution=distribution,
        )
        self.ciss_weight = ciss_weight
        self._ciss = None
        self._ciss_coefficient = None
    
    def fit_with_ciss(
        self,
        returns: pd.Series,
        sentiment: Optional[pd.Series] = None,
        ciss: Optional[pd.Series] = None,
        ciss_transform: Literal["raw", "log", "zscore", "rank"] = "raw",
    ) -> 'GARCHMIDASWithCISSResult':
        """
        Fit GARCH-MIDAS with both sentiment and CISS.
        
        Args:
            returns: Daily returns series
            sentiment: Sentiment index (-1 to 1)
            ciss: ECB CISS series (0 to 1)
            ciss_transform: How to transform CISS before fitting
            
        Returns:
            GARCHMIDASWithCISSResult with extended outputs
        """
        self._returns = returns.dropna()
        self._sentiment = sentiment
        self._ciss = ciss
        
        # Transform CISS if provided
        if ciss is not None:
            ciss_aligned = ciss.reindex(self._returns.index, method='ffill')
            
            if ciss_transform == "log":
                ciss_transformed = np.log(ciss_aligned + 0.001)
            elif ciss_transform == "zscore":
                ciss_transformed = (ciss_aligned - ciss_aligned.mean()) / ciss_aligned.std()
            elif ciss_transform == "rank":
                ciss_transformed = ciss_aligned.rank(pct=True)
            else:  # raw
                ciss_transformed = ciss_aligned
        else:
            ciss_transformed = None
        
        # Compute combined exogenous variable
        if sentiment is not None and ciss_transformed is not None:
            # Transform sentiment to risk scale (negative sentiment = high risk)
            sent_aligned = sentiment.reindex(self._returns.index, method='ffill').fillna(0)
            sentiment_risk = (1 - sent_aligned) / 2  # Map [-1,1] to [1,0] (inverted)
            
            # Combine with CISS using weight
            combined = (
                self.ciss_weight * ciss_transformed.fillna(ciss_transformed.mean()) +
                (1 - self.ciss_weight) * sentiment_risk
            )
        elif ciss_transformed is not None:
            combined = ciss_transformed
        elif sentiment is not None:
            combined = sentiment
        else:
            combined = None
        
        # Fit base model with combined exogenous
        base_result = self.fit(returns=self._returns, sentiment=combined)
        
        # Estimate separate coefficients for CISS
        ciss_coef = None
        if ciss is not None and base_result.convergence:
            try:
                log_var = np.log(base_result.conditional_volatility ** 2)
                X = np.column_stack([
                    np.ones(len(self._returns)),
                    ciss_aligned.reindex(self._returns.index, method='ffill').fillna(0).values
                ])
                y = log_var.values
                valid = ~(np.isnan(X).any(axis=1) | np.isnan(y))
                
                if valid.sum() > 10:
                    coefs = np.linalg.lstsq(X[valid], y[valid], rcond=None)[0]
                    ciss_coef = float(coefs[1])
            except Exception as e:
                logger.warning(f"Could not estimate CISS coefficient: {e}")
        
        self._ciss_coefficient = ciss_coef
        
        # Return extended result
        return GARCHMIDASWithCISSResult(
            conditional_volatility=base_result.conditional_volatility,
            long_run_volatility=base_result.long_run_volatility,
            short_run_volatility=base_result.short_run_volatility,
            params=base_result.params,
            sentiment_coefficient=base_result.sentiment_coefficient,
            ciss_coefficient=ciss_coef,
            combined_coefficient=base_result.sentiment_coefficient,  # Combined effect
            aic=base_result.aic,
            bic=base_result.bic,
            log_likelihood=base_result.log_likelihood,
            residuals=base_result.residuals,
            midas_weights=base_result.midas_weights,
            convergence=base_result.convergence,
            ciss_weight=self.ciss_weight,
        )
    
    def get_volatility_decomposition(self) -> pd.DataFrame:
        """
        Decompose volatility into sentiment and CISS contributions.
        
        Returns:
            DataFrame with columns:
            - total_vol: Total conditional volatility
            - short_run: GARCH component
            - long_run: MIDAS component
            - sentiment_contrib: Estimated sentiment contribution
            - ciss_contrib: Estimated CISS contribution
        """
        if self._result is None:
            raise ValueError("Model must be fitted first")
        
        result = pd.DataFrame(index=self._result.conditional_volatility.index)
        result['total_vol'] = self._result.conditional_volatility
        result['short_run'] = self._result.short_run_volatility
        result['long_run'] = self._result.long_run_volatility
        
        # Estimate contributions using fitted coefficients
        if self._sentiment is not None:
            sent_aligned = self._sentiment.reindex(result.index, method='ffill').fillna(0)
            sent_coef = self._result.sentiment_coefficient or 0
            result['sentiment_contrib'] = sent_aligned * sent_coef * (1 - self.ciss_weight)
        
        if self._ciss is not None:
            ciss_aligned = self._ciss.reindex(result.index, method='ffill').fillna(0)
            ciss_coef = self._ciss_coefficient or 0
            result['ciss_contrib'] = ciss_aligned * ciss_coef * self.ciss_weight
        
        return result


@dataclass
class GARCHMIDASWithCISSResult(GARCHMIDASResult):
    """Extended result with CISS-specific outputs."""
    
    ciss_coefficient: Optional[float] = None
    combined_coefficient: Optional[float] = None
    ciss_weight: float = 0.5
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        base = super().to_dict()
        base.update({
            "ciss_coefficient": self.ciss_coefficient,
            "combined_coefficient": self.combined_coefficient,
            "ciss_weight": self.ciss_weight,
        })
        return base
    
    def summary(self) -> str:
        """Generate model summary."""
        lines = [
            "GARCH-MIDAS with CISS Model Results",
            "=" * 45,
            "",
            "GARCH Parameters:",
            f"  ω (omega):  {self.params.get('omega', 'N/A'):.6f}",
            f"  α (alpha):  {self.params.get('alpha', 'N/A'):.6f}",
            f"  β (beta):   {self.params.get('beta', 'N/A'):.6f}",
            "",
            "MIDAS Exogenous Coefficients:",
            f"  Sentiment:  {self.sentiment_coefficient or 'N/A'}",
            f"  CISS:       {self.ciss_coefficient or 'N/A'}",
            f"  Combined:   {self.combined_coefficient or 'N/A'}",
            f"  CISS Weight: {self.ciss_weight:.2f}",
            "",
            "Model Fit:",
            f"  Log-Likelihood: {self.log_likelihood:.2f}",
            f"  AIC: {self.aic:.2f}",
            f"  BIC: {self.bic:.2f}",
            f"  Converged: {self.convergence}",
            "",
            "Volatility Statistics:",
            f"  Mean: {self.conditional_volatility.mean():.4f}",
            f"  Std:  {self.conditional_volatility.std():.4f}",
            f"  Max:  {self.conditional_volatility.max():.4f}",
        ]
        return "\n".join(lines)
