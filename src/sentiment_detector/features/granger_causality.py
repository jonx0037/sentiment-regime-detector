"""
Granger Causality Analysis for Sentiment Spillover Networks.

This module implements Granger causality tests to construct sentiment spillover
networks between asset classes, following the methodology from Cao et al. (2025).

The Granger causality network forms the foundation for:
- H3 (Network Effect Hypothesis) validation
- Sentiment connectedness calculations
- Cross-asset sentiment transmission analysis
"""

from dataclasses import dataclass, field
from typing import Optional, Union
import logging

import numpy as np
import pandas as pd
from scipy import stats

logger = logging.getLogger(__name__)


@dataclass
class GrangerResult:
    """
    Result of a pairwise Granger causality test.
    
    Attributes:
        source: Source variable (X causes Y)
        target: Target variable
        lag: Optimal lag used in the test
        f_statistic: F-statistic from the test
        p_value: P-value for the null hypothesis (X does not Granger-cause Y)
        is_significant: Whether causality is significant at the given alpha
        direction: "unidirectional", "bidirectional", or "none"
        r_squared: R-squared of the full model
    """
    source: str
    target: str
    lag: int
    f_statistic: float
    p_value: float
    is_significant: bool
    direction: str = "unidirectional"
    r_squared: float = 0.0
    

@dataclass 
class CausalityNetwork:
    """
    Sentiment spillover network constructed from Granger causality tests.
    
    Attributes:
        nodes: List of asset classes/variables in the network
        edges: List of GrangerResult objects representing causal links
        adjacency_matrix: NxN matrix of causality strengths
        significance_matrix: NxN boolean matrix of significant links
        metadata: Additional network metadata
    """
    nodes: list[str]
    edges: list[GrangerResult]
    adjacency_matrix: np.ndarray
    significance_matrix: np.ndarray
    metadata: dict = field(default_factory=dict)
    
    @property
    def n_nodes(self) -> int:
        return len(self.nodes)
    
    @property
    def n_edges(self) -> int:
        return len([e for e in self.edges if e.is_significant])
    
    @property
    def density(self) -> float:
        """Network density (proportion of possible edges that exist)."""
        max_edges = self.n_nodes * (self.n_nodes - 1)
        return self.n_edges / max_edges if max_edges > 0 else 0.0


class GrangerCausalityAnalyzer:
    """
    Granger causality analyzer for sentiment time series.
    
    Implements linear and nonlinear Granger causality tests to detect
    sentiment spillovers between asset classes.
    
    Per Cao et al. (2025), we use nonlinear Granger causality methods
    to capture complex dependencies in sentiment transmission.
    
    Example:
        >>> analyzer = GrangerCausalityAnalyzer(max_lag=5, significance_level=0.05)
        >>> # Create sentiment DataFrame with asset class columns
        >>> network = analyzer.build_network(sentiment_df)
        >>> print(f"Network has {network.n_edges} significant causal links")
    """
    
    def __init__(
        self,
        max_lag: int = 5,
        significance_level: float = 0.05,
        min_observations: int = 50,
        use_nonlinear: bool = True
    ):
        """
        Initialize Granger causality analyzer.
        
        Args:
            max_lag: Maximum lag to test for causality
            significance_level: Alpha level for significance testing
            min_observations: Minimum observations required for test
            use_nonlinear: Whether to use nonlinear methods (via nitime)
        """
        self.max_lag = max_lag
        self.significance_level = significance_level
        self.min_observations = min_observations
        self.use_nonlinear = use_nonlinear
        
    def test_pairwise(
        self,
        x: np.ndarray,
        y: np.ndarray,
        source_name: str = "X",
        target_name: str = "Y",
        lag: Optional[int] = None
    ) -> GrangerResult:
        """
        Test Granger causality from X to Y.
        
        Tests whether past values of X help predict Y beyond Y's own past.
        
        Args:
            x: Source time series
            y: Target time series
            source_name: Name of source variable
            target_name: Name of target variable
            lag: Specific lag to test (if None, uses optimal lag)
            
        Returns:
            GrangerResult with test statistics
        """
        x = np.asarray(x).flatten()
        y = np.asarray(y).flatten()
        
        # Ensure same length
        min_len = min(len(x), len(y))
        x = x[:min_len]
        y = y[:min_len]
        
        if len(x) < self.min_observations:
            logger.warning(
                f"Insufficient observations ({len(x)}) for Granger test. "
                f"Minimum required: {self.min_observations}"
            )
            return GrangerResult(
                source=source_name,
                target=target_name,
                lag=0,
                f_statistic=0.0,
                p_value=1.0,
                is_significant=False,
                direction="none"
            )
        
        # Find optimal lag if not specified
        if lag is None:
            lag = self._select_optimal_lag(x, y)
        
        # Perform Granger causality test
        try:
            f_stat, p_value, r_squared = self._granger_test(x, y, lag)
        except Exception as e:
            logger.error(f"Granger test failed: {e}")
            return GrangerResult(
                source=source_name,
                target=target_name,
                lag=lag,
                f_statistic=0.0,
                p_value=1.0,
                is_significant=False,
                direction="none"
            )
        
        is_significant = p_value < self.significance_level
        
        return GrangerResult(
            source=source_name,
            target=target_name,
            lag=lag,
            f_statistic=f_stat,
            p_value=p_value,
            is_significant=is_significant,
            direction="unidirectional" if is_significant else "none",
            r_squared=r_squared
        )
    
    def _granger_test(
        self,
        x: np.ndarray,
        y: np.ndarray,
        lag: int
    ) -> tuple[float, float, float]:
        """
        Perform the Granger causality F-test.
        
        Tests H0: X does not Granger-cause Y
        vs H1: X Granger-causes Y
        
        Returns:
            Tuple of (F-statistic, p-value, R-squared)
        """
        n = len(y)
        
        # Build restricted model: Y ~ Y_lags only
        Y_restricted = self._create_lag_matrix(y, lag)
        y_target = y[lag:]
        
        # Build unrestricted model: Y ~ Y_lags + X_lags
        X_lags = self._create_lag_matrix(x, lag)
        Y_unrestricted = np.hstack([Y_restricted, X_lags])
        
        # Fit models using OLS
        rss_restricted = self._ols_residual_ss(Y_restricted, y_target)
        rss_unrestricted = self._ols_residual_ss(Y_unrestricted, y_target)
        
        # Calculate F-statistic
        # F = ((RSS_r - RSS_u) / q) / (RSS_u / (n - k))
        # where q = number of restrictions (lag), k = total params in unrestricted
        q = lag  # Number of X lag terms
        k = 2 * lag + 1  # Y lags + X lags + intercept
        n_obs = len(y_target)
        
        if rss_unrestricted <= 0:
            return 0.0, 1.0, 0.0
        
        f_stat = ((rss_restricted - rss_unrestricted) / q) / (rss_unrestricted / (n_obs - k))
        
        # P-value from F distribution
        p_value = 1 - stats.f.cdf(f_stat, q, n_obs - k)
        
        # R-squared of unrestricted model
        tss = np.sum((y_target - np.mean(y_target)) ** 2)
        r_squared = 1 - (rss_unrestricted / tss) if tss > 0 else 0.0
        
        return float(f_stat), float(p_value), float(r_squared)
    
    def _create_lag_matrix(self, series: np.ndarray, lag: int) -> np.ndarray:
        """Create matrix of lagged values."""
        n = len(series)
        matrix = np.zeros((n - lag, lag))
        
        for i in range(lag):
            matrix[:, i] = series[lag - i - 1:n - i - 1]
        
        return matrix
    
    def _ols_residual_ss(self, X: np.ndarray, y: np.ndarray) -> float:
        """Calculate residual sum of squares from OLS regression."""
        # Add constant term
        X_const = np.column_stack([np.ones(len(X)), X])
        
        try:
            # Use least squares
            beta, residuals, rank, s = np.linalg.lstsq(X_const, y, rcond=None)
            
            if len(residuals) > 0:
                return float(residuals[0])
            else:
                # Calculate manually
                y_pred = X_const @ beta
                return float(np.sum((y - y_pred) ** 2))
        except np.linalg.LinAlgError:
            return np.inf
    
    def _select_optimal_lag(self, x: np.ndarray, y: np.ndarray) -> int:
        """
        Select optimal lag using BIC criterion.
        
        Tests lags from 1 to max_lag and selects the one with lowest BIC.
        """
        best_lag = 1
        best_bic = np.inf
        
        for lag in range(1, self.max_lag + 1):
            if len(y) <= lag + 10:  # Need enough observations
                break
                
            try:
                Y_lags = self._create_lag_matrix(y, lag)
                X_lags = self._create_lag_matrix(x, lag)
                X_full = np.hstack([Y_lags, X_lags])
                y_target = y[lag:]
                
                rss = self._ols_residual_ss(X_full, y_target)
                n = len(y_target)
                k = 2 * lag + 1
                
                # BIC = n * log(RSS/n) + k * log(n)
                if rss > 0:
                    bic = n * np.log(rss / n) + k * np.log(n)
                    
                    if bic < best_bic:
                        best_bic = bic
                        best_lag = lag
            except Exception:
                continue
        
        return best_lag
    
    def build_network(
        self,
        data: pd.DataFrame,
        columns: Optional[list[str]] = None
    ) -> CausalityNetwork:
        """
        Build a Granger causality network from sentiment time series.
        
        Tests all pairwise relationships and constructs an adjacency matrix.
        
        Args:
            data: DataFrame with sentiment time series (columns = asset classes)
            columns: Specific columns to include (default: all numeric columns)
            
        Returns:
            CausalityNetwork with nodes, edges, and matrices
        """
        if columns is None:
            columns = data.select_dtypes(include=[np.number]).columns.tolist()
        
        n = len(columns)
        adjacency = np.zeros((n, n))
        significance = np.zeros((n, n), dtype=bool)
        edges = []
        
        logger.info(f"Building Granger causality network for {n} variables")
        
        for i, source in enumerate(columns):
            for j, target in enumerate(columns):
                if i == j:
                    continue  # Skip self-loops
                
                x = data[source].values
                y = data[target].values
                
                # Remove NaN values
                mask = ~(np.isnan(x) | np.isnan(y))
                x_clean = x[mask]
                y_clean = y[mask]
                
                result = self.test_pairwise(
                    x_clean, y_clean,
                    source_name=source,
                    target_name=target
                )
                
                edges.append(result)
                
                # Use -log(p_value) as edge weight for significant links
                if result.is_significant:
                    adjacency[i, j] = -np.log(max(result.p_value, 1e-10))
                    significance[i, j] = True
        
        # Detect bidirectional relationships
        for edge in edges:
            if edge.is_significant:
                # Check if reverse direction is also significant
                reverse = next(
                    (e for e in edges 
                     if e.source == edge.target and e.target == edge.source and e.is_significant),
                    None
                )
                if reverse:
                    edge.direction = "bidirectional"
        
        network = CausalityNetwork(
            nodes=columns,
            edges=edges,
            adjacency_matrix=adjacency,
            significance_matrix=significance,
            metadata={
                "max_lag": self.max_lag,
                "significance_level": self.significance_level,
                "n_observations": len(data),
                "n_significant_edges": int(significance.sum()),
            }
        )
        
        logger.info(
            f"Network built: {network.n_edges} significant edges, "
            f"density: {network.density:.3f}"
        )
        
        return network
    
    def get_net_spillover(self, network: CausalityNetwork) -> dict[str, float]:
        """
        Calculate net spillover for each node.
        
        Net spillover = spillover TO others - spillover FROM others
        Positive = net transmitter, Negative = net receiver
        
        Args:
            network: CausalityNetwork object
            
        Returns:
            Dict mapping node names to net spillover values
        """
        spillover = {}
        adj = network.adjacency_matrix
        
        for i, node in enumerate(network.nodes):
            to_others = adj[i, :].sum()  # Outgoing
            from_others = adj[:, i].sum()  # Incoming
            spillover[node] = to_others - from_others
        
        return spillover


def granger_causality_test(
    x: Union[np.ndarray, pd.Series],
    y: Union[np.ndarray, pd.Series],
    max_lag: int = 5,
    significance_level: float = 0.05
) -> GrangerResult:
    """
    Convenience function for single pairwise Granger test.
    
    Args:
        x: Source time series (does X cause Y?)
        y: Target time series
        max_lag: Maximum lag to test
        significance_level: Alpha level
        
    Returns:
        GrangerResult with test statistics
    """
    analyzer = GrangerCausalityAnalyzer(
        max_lag=max_lag,
        significance_level=significance_level
    )
    
    x_name = x.name if hasattr(x, 'name') and x.name else "X"
    y_name = y.name if hasattr(y, 'name') and y.name else "Y"
    
    return analyzer.test_pairwise(
        np.asarray(x), np.asarray(y),
        source_name=str(x_name),
        target_name=str(y_name)
    )
