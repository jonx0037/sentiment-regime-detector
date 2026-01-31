"""
Transfer Entropy Analysis for Sentiment Information Flow.

This module implements Transfer Entropy measures to quantify directed
information flow between sentiment time series, following Caferra (2022).

Transfer Entropy captures nonlinear dependencies that Granger causality
may miss, providing a more complete picture of sentiment transmission.

Key features:
- Shannon Transfer Entropy (standard)
- Rényi Transfer Entropy (generalized)
- Effective Transfer Entropy (bias-corrected)
"""

from dataclasses import dataclass, field
from typing import Optional, Union
import logging

import numpy as np
import pandas as pd
from scipy import stats

logger = logging.getLogger(__name__)

# Try to import pyinform for entropy calculations
# Note: pyinform has known compatibility issues with Apple Silicon (ARM)
PYINFORM_AVAILABLE = False
pyinform_te = None

try:
    import pyinform
    from pyinform import transfer_entropy as pyinform_te
    PYINFORM_AVAILABLE = True
except (ImportError, OSError) as e:
    # OSError occurs when the C library is incompatible (e.g., x86 on ARM)
    logger.warning(f"pyinform not available ({type(e).__name__}). Using fallback entropy calculations.")


@dataclass
class TransferEntropyResult:
    """
    Result of a transfer entropy calculation.
    
    Attributes:
        source: Source variable (information sender)
        target: Target variable (information receiver)
        transfer_entropy: TE value (bits of information transferred)
        normalized_te: TE normalized by target entropy
        effective_te: Bias-corrected TE
        p_value: Statistical significance
        is_significant: Whether flow is significant at given alpha
        history_length: History length (k) used
    """
    source: str
    target: str
    transfer_entropy: float
    normalized_te: float
    effective_te: float
    p_value: float
    is_significant: bool
    history_length: int
    

@dataclass
class InformationFlowNetwork:
    """
    Information flow network based on Transfer Entropy.
    
    Attributes:
        nodes: List of variables in the network
        flows: List of TransferEntropyResult objects
        adjacency_matrix: NxN matrix of TE values
        significance_matrix: NxN boolean matrix
        metadata: Network statistics
    """
    nodes: list[str]
    flows: list[TransferEntropyResult]
    adjacency_matrix: np.ndarray
    significance_matrix: np.ndarray
    metadata: dict = field(default_factory=dict)
    
    @property
    def total_flow(self) -> float:
        """Total information flow in the network."""
        return float(self.adjacency_matrix.sum())
    
    @property
    def n_significant_flows(self) -> int:
        """Number of significant information flows."""
        return int(self.significance_matrix.sum())


class TransferEntropyAnalyzer:
    """
    Transfer Entropy analyzer for sentiment time series.
    
    Implements Shannon and Rényi Transfer Entropy to measure directed
    information flow between asset class sentiments.
    
    Per Caferra (2022), Transfer Entropy captures asymmetric information
    transmission that reflects genuine causality in financial sentiment.
    
    Example:
        >>> analyzer = TransferEntropyAnalyzer(history_length=3)
        >>> # For discretized sentiment series
        >>> te = analyzer.calculate_te(source_sentiment, target_sentiment)
        >>> print(f"Information flow: {te.transfer_entropy:.4f} bits")
    """
    
    def __init__(
        self,
        history_length: int = 3,
        significance_level: float = 0.05,
        n_permutations: int = 100,
        n_bins: int = 5
    ):
        """
        Initialize Transfer Entropy analyzer.
        
        Args:
            history_length: History length k for TE calculation
            significance_level: Alpha level for significance testing
            n_permutations: Number of permutations for significance testing
            n_bins: Number of bins for discretization
        """
        self.history_length = history_length
        self.significance_level = significance_level
        self.n_permutations = n_permutations
        self.n_bins = n_bins
        
    def discretize(
        self,
        series: np.ndarray,
        n_bins: Optional[int] = None
    ) -> np.ndarray:
        """
        Discretize continuous series into symbolic representation.
        
        Uses equal-frequency binning to ensure each bin has similar counts.
        
        Args:
            series: Continuous time series
            n_bins: Number of bins (default: self.n_bins)
            
        Returns:
            Discretized series with values 0 to n_bins-1
        """
        if n_bins is None:
            n_bins = self.n_bins
            
        series = np.asarray(series).flatten()
        
        # Remove NaN values for binning
        valid_mask = ~np.isnan(series)
        valid_values = series[valid_mask]
        
        if len(valid_values) == 0:
            return np.zeros(len(series), dtype=int)
        
        # Equal-frequency binning using percentiles
        percentiles = np.linspace(0, 100, n_bins + 1)
        bin_edges = np.percentile(valid_values, percentiles)
        
        # Ensure unique edges
        bin_edges = np.unique(bin_edges)
        
        # Digitize
        discretized = np.digitize(series, bin_edges[1:-1])
        
        return discretized.astype(int)
    
    def calculate_te(
        self,
        source: np.ndarray,
        target: np.ndarray,
        source_name: str = "Source",
        target_name: str = "Target",
        discretize: bool = True
    ) -> TransferEntropyResult:
        """
        Calculate Transfer Entropy from source to target.
        
        TE(X→Y) = H(Y_t | Y_past) - H(Y_t | Y_past, X_past)
        
        Measures how much knowing the past of X reduces uncertainty
        about the future of Y, beyond what Y's own past tells us.
        
        Args:
            source: Source time series
            target: Target time series
            source_name: Name for source variable
            target_name: Name for target variable
            discretize: Whether to discretize continuous series
            
        Returns:
            TransferEntropyResult with TE value and statistics
        """
        source = np.asarray(source).flatten()
        target = np.asarray(target).flatten()
        
        # Ensure same length
        min_len = min(len(source), len(target))
        source = source[:min_len]
        target = target[:min_len]
        
        # Remove NaN values
        mask = ~(np.isnan(source) | np.isnan(target))
        source = source[mask]
        target = target[mask]
        
        if len(source) < self.history_length + 10:
            logger.warning(f"Insufficient data for TE calculation: {len(source)} points")
            return TransferEntropyResult(
                source=source_name,
                target=target_name,
                transfer_entropy=0.0,
                normalized_te=0.0,
                effective_te=0.0,
                p_value=1.0,
                is_significant=False,
                history_length=self.history_length
            )
        
        # Discretize if needed
        if discretize:
            source = self.discretize(source)
            target = self.discretize(target)
        else:
            source = source.astype(int)
            target = target.astype(int)
        
        # Calculate Transfer Entropy
        if PYINFORM_AVAILABLE:
            te = self._calculate_te_pyinform(source, target)
        else:
            te = self._calculate_te_manual(source, target)
        
        # Calculate normalized TE
        target_entropy = self._calculate_entropy(target)
        normalized_te = te / target_entropy if target_entropy > 0 else 0.0
        
        # Calculate effective TE with permutation test
        effective_te, p_value = self._permutation_test(source, target, te)
        
        is_significant = p_value < self.significance_level
        
        return TransferEntropyResult(
            source=source_name,
            target=target_name,
            transfer_entropy=te,
            normalized_te=normalized_te,
            effective_te=effective_te,
            p_value=p_value,
            is_significant=is_significant,
            history_length=self.history_length
        )
    
    def _calculate_te_pyinform(self, source: np.ndarray, target: np.ndarray) -> float:
        """Calculate TE using pyinform library."""
        try:
            te = pyinform_te.transfer_entropy(
                source, target, 
                k=self.history_length
            )
            return float(te)
        except Exception as e:
            logger.warning(f"pyinform TE failed: {e}. Using manual calculation.")
            return self._calculate_te_manual(source, target)
    
    def _calculate_te_manual(self, source: np.ndarray, target: np.ndarray) -> float:
        """
        Calculate Transfer Entropy manually.
        
        TE(X→Y) = Σ p(y_t, y_past, x_past) * log2(p(y_t|y_past,x_past) / p(y_t|y_past))
        """
        k = self.history_length
        n = len(target)
        
        if n <= k:
            return 0.0
        
        # Build joint observations
        # y_t, y_{t-1:t-k}, x_{t-1:t-k}
        y_future = target[k:]
        y_past = np.column_stack([target[k-i-1:n-i-1] for i in range(k)])
        x_past = np.column_stack([source[k-i-1:n-i-1] for i in range(k)])
        
        # Count joint occurrences
        # For efficiency, use hash-based counting
        te = 0.0
        
        # Create joint state tuples
        n_obs = len(y_future)
        
        # Count p(y_t, y_past, x_past)
        joint_counts = {}
        y_past_counts = {}
        y_past_x_past_counts = {}
        y_t_y_past_counts = {}
        
        for i in range(n_obs):
            y_t = y_future[i]
            y_p = tuple(y_past[i])
            x_p = tuple(x_past[i])
            
            joint_key = (y_t, y_p, x_p)
            joint_counts[joint_key] = joint_counts.get(joint_key, 0) + 1
            
            y_past_counts[y_p] = y_past_counts.get(y_p, 0) + 1
            
            y_past_x_past_key = (y_p, x_p)
            y_past_x_past_counts[y_past_x_past_key] = y_past_x_past_counts.get(y_past_x_past_key, 0) + 1
            
            y_t_y_past_key = (y_t, y_p)
            y_t_y_past_counts[y_t_y_past_key] = y_t_y_past_counts.get(y_t_y_past_key, 0) + 1
        
        # Calculate TE
        for joint_key, count in joint_counts.items():
            y_t, y_p, x_p = joint_key
            
            p_joint = count / n_obs
            
            y_past_x_past_key = (y_p, x_p)
            p_y_past_x_past = y_past_x_past_counts[y_past_x_past_key] / n_obs
            
            p_y_past = y_past_counts[y_p] / n_obs
            
            y_t_y_past_key = (y_t, y_p)
            p_y_t_y_past = y_t_y_past_counts[y_t_y_past_key] / n_obs
            
            # p(y_t | y_past, x_past) = p(y_t, y_past, x_past) / p(y_past, x_past)
            p_y_t_given_both = p_joint / p_y_past_x_past if p_y_past_x_past > 0 else 0
            
            # p(y_t | y_past) = p(y_t, y_past) / p(y_past)
            p_y_t_given_y_past = p_y_t_y_past / p_y_past if p_y_past > 0 else 0
            
            if p_y_t_given_both > 0 and p_y_t_given_y_past > 0:
                te += p_joint * np.log2(p_y_t_given_both / p_y_t_given_y_past)
        
        return max(0.0, te)  # TE should be non-negative
    
    def _calculate_entropy(self, series: np.ndarray) -> float:
        """Calculate Shannon entropy of a discrete series."""
        values, counts = np.unique(series, return_counts=True)
        probs = counts / len(series)
        entropy = -np.sum(probs * np.log2(probs + 1e-10))
        return float(entropy)
    
    def _permutation_test(
        self,
        source: np.ndarray,
        target: np.ndarray,
        observed_te: float
    ) -> tuple[float, float]:
        """
        Permutation test for TE significance.
        
        Shuffles the source series to destroy temporal structure
        and compares observed TE to null distribution.
        
        Returns:
            Tuple of (effective_te, p_value)
        """
        null_tes = []
        
        for _ in range(self.n_permutations):
            # Shuffle source to break temporal relationship
            shuffled_source = np.random.permutation(source)
            
            if PYINFORM_AVAILABLE:
                null_te = self._calculate_te_pyinform(shuffled_source, target)
            else:
                null_te = self._calculate_te_manual(shuffled_source, target)
            
            null_tes.append(null_te)
        
        null_tes = np.array(null_tes)
        
        # Effective TE = observed - mean(null)
        effective_te = observed_te - np.mean(null_tes)
        
        # P-value: proportion of null values >= observed
        p_value = np.mean(null_tes >= observed_te)
        
        return float(effective_te), float(p_value)
    
    def calculate_renyi_te(
        self,
        source: np.ndarray,
        target: np.ndarray,
        alpha: float = 2.0,
        source_name: str = "Source",
        target_name: str = "Target"
    ) -> TransferEntropyResult:
        """
        Calculate Rényi Transfer Entropy.
        
        Rényi TE generalizes Shannon TE with parameter alpha:
        - alpha → 1: Shannon TE
        - alpha = 2: Emphasizes common states
        - alpha > 2: Emphasizes most probable states
        
        Per Caferra (2022), Rényi TE with alpha=2 is useful for
        detecting strong information flows in financial data.
        
        Args:
            source: Source time series
            target: Target time series
            alpha: Rényi parameter (default: 2.0)
            source_name: Name for source variable
            target_name: Name for target variable
            
        Returns:
            TransferEntropyResult with Rényi TE
        """
        source = np.asarray(source).flatten()
        target = np.asarray(target).flatten()
        
        # Discretize
        source = self.discretize(source)
        target = self.discretize(target)
        
        # For alpha=2, use quadratic Rényi entropy
        # This is a simplified implementation
        k = self.history_length
        n = len(target)
        
        if n <= k:
            return TransferEntropyResult(
                source=source_name,
                target=target_name,
                transfer_entropy=0.0,
                normalized_te=0.0,
                effective_te=0.0,
                p_value=1.0,
                is_significant=False,
                history_length=k
            )
        
        # Fall back to Shannon TE with alpha adjustment
        # This is an approximation; full Rényi TE requires more complex computation
        shannon_te = self._calculate_te_manual(source, target)
        
        # Approximate Rényi scaling factor
        if alpha > 1:
            renyi_te = shannon_te / (alpha - 1) * np.log2(alpha)
        else:
            renyi_te = shannon_te
        
        effective_te, p_value = self._permutation_test(source, target, renyi_te)
        
        return TransferEntropyResult(
            source=source_name,
            target=target_name,
            transfer_entropy=renyi_te,
            normalized_te=renyi_te / self._calculate_entropy(target) if self._calculate_entropy(target) > 0 else 0,
            effective_te=effective_te,
            p_value=p_value,
            is_significant=p_value < self.significance_level,
            history_length=k
        )
    
    def build_network(
        self,
        data: pd.DataFrame,
        columns: Optional[list[str]] = None
    ) -> InformationFlowNetwork:
        """
        Build an information flow network from sentiment time series.
        
        Args:
            data: DataFrame with sentiment time series
            columns: Specific columns to include
            
        Returns:
            InformationFlowNetwork with TE-based adjacency
        """
        if columns is None:
            columns = data.select_dtypes(include=[np.number]).columns.tolist()
        
        n = len(columns)
        adjacency = np.zeros((n, n))
        significance = np.zeros((n, n), dtype=bool)
        flows = []
        
        logger.info(f"Building Transfer Entropy network for {n} variables")
        
        for i, source in enumerate(columns):
            for j, target in enumerate(columns):
                if i == j:
                    continue
                
                x = data[source].values
                y = data[target].values
                
                result = self.calculate_te(
                    x, y,
                    source_name=source,
                    target_name=target
                )
                
                flows.append(result)
                adjacency[i, j] = result.transfer_entropy
                significance[i, j] = result.is_significant
        
        network = InformationFlowNetwork(
            nodes=columns,
            flows=flows,
            adjacency_matrix=adjacency,
            significance_matrix=significance,
            metadata={
                "history_length": self.history_length,
                "n_bins": self.n_bins,
                "n_permutations": self.n_permutations,
                "significance_level": self.significance_level,
                "total_flow": float(adjacency.sum()),
                "n_significant_flows": int(significance.sum()),
            }
        )
        
        logger.info(
            f"Network built: {network.n_significant_flows} significant flows, "
            f"total flow: {network.total_flow:.4f} bits"
        )
        
        return network


def transfer_entropy(
    source: Union[np.ndarray, pd.Series],
    target: Union[np.ndarray, pd.Series],
    history_length: int = 3,
    significance_level: float = 0.05
) -> TransferEntropyResult:
    """
    Convenience function for single Transfer Entropy calculation.
    
    Args:
        source: Source time series
        target: Target time series
        history_length: History length k
        significance_level: Alpha level
        
    Returns:
        TransferEntropyResult with TE statistics
    """
    analyzer = TransferEntropyAnalyzer(
        history_length=history_length,
        significance_level=significance_level
    )
    
    source_name = source.name if hasattr(source, 'name') and source.name else "Source"
    target_name = target.name if hasattr(target, 'name') and target.name else "Target"
    
    return analyzer.calculate_te(
        np.asarray(source), np.asarray(target),
        source_name=str(source_name),
        target_name=str(target_name)
    )
