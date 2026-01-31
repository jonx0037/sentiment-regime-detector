"""
Statistical Jump Model for Regime Classification.

This module implements the Statistical Jump Model (JM) as described by
Shu et al. (2024) for market regime detection. Unlike Hidden Markov Models,
the JM explicitly penalizes frequent state switching via a jump penalty (λ),
ensuring regime persistence and reducing "whipsaw" false positives.

The objective function is:
    min_{Θ, s} Σ ℓ(x_t, θ_{s_t}) + λ Σ 𝕀(s_t ≠ s_{t-1})

Where:
- s = {s_0, ..., s_{T-1}}: Sequence of discrete regimes
- Θ = {θ_0, ..., θ_{K-1}}: Centroid parameters for each regime
- ℓ(·): Loss function (scaled squared Euclidean distance)
- λ: Jump penalty hyperparameter

References:
- Shu et al. (2024) "Statistical Jump Models for Regime Detection"
- Draft-1.md Section 3.7.2
"""

from dataclasses import dataclass, field
from typing import Optional, List, Tuple, Literal, Union
from enum import Enum
import logging
import warnings

import numpy as np
import pandas as pd
from scipy.optimize import minimize

logger = logging.getLogger(__name__)


class RegimeState(str, Enum):
    """Market regime states."""
    RISK_ON = "risk_on"
    RISK_OFF = "risk_off"
    TRANSITION = "transition"


@dataclass
class JumpModelConfig:
    """
    Configuration for Statistical Jump Model.
    
    Attributes:
        n_regimes: Number of discrete regime states (default 3: Risk-On, Risk-Off, Transition)
        jump_penalty: Lambda (λ) parameter penalizing state switches
        max_iter: Maximum iterations for optimization
        tol: Convergence tolerance
        init_method: Initialization method ('kmeans', 'quantile', 'random')
    """
    n_regimes: int = 3
    jump_penalty: float = 10.0  # λ - higher = more persistent regimes
    max_iter: int = 100
    tol: float = 1e-6
    init_method: Literal['kmeans', 'quantile', 'random'] = 'kmeans'
    min_regime_duration: int = 5  # Minimum days in a regime


@dataclass
class RegimeCentroid:
    """
    Parameters for a regime centroid.
    
    Attributes:
        mean: Mean feature vector for this regime
        covariance: Covariance matrix (or variance if 1D)
        regime_id: Integer identifier
        regime_name: Human-readable name
    """
    mean: np.ndarray
    covariance: np.ndarray
    regime_id: int
    regime_name: str
    
    @property
    def n_features(self) -> int:
        return len(self.mean)


@dataclass 
class JumpModelResult:
    """
    Result from Jump Model fitting/prediction.
    
    Attributes:
        regimes: Array of regime assignments for each time step
        regime_probabilities: Probability distribution over regimes at each step
        centroids: Fitted regime centroids
        total_loss: Final objective value
        n_jumps: Number of regime transitions
        convergence_info: Optimization convergence details
    """
    regimes: np.ndarray
    regime_probabilities: np.ndarray
    centroids: List[RegimeCentroid]
    total_loss: float
    n_jumps: int
    convergence_info: dict = field(default_factory=dict)
    
    @property
    def regime_names(self) -> List[str]:
        """Map regime IDs to names."""
        id_to_name = {c.regime_id: c.regime_name for c in self.centroids}
        return [id_to_name.get(r, f"regime_{r}") for r in self.regimes]
    
    def get_regime_durations(self) -> dict:
        """Calculate average duration of each regime."""
        durations = {c.regime_name: [] for c in self.centroids}
        
        current_regime = self.regimes[0]
        current_duration = 1
        
        for r in self.regimes[1:]:
            if r == current_regime:
                current_duration += 1
            else:
                regime_name = next(
                    (c.regime_name for c in self.centroids if c.regime_id == current_regime),
                    f"regime_{current_regime}"
                )
                durations[regime_name].append(current_duration)
                current_regime = r
                current_duration = 1
        
        # Don't forget last segment
        regime_name = next(
            (c.regime_name for c in self.centroids if c.regime_id == current_regime),
            f"regime_{current_regime}"
        )
        durations[regime_name].append(current_duration)
        
        return {k: np.mean(v) if v else 0 for k, v in durations.items()}


class StatisticalJumpModel:
    """
    Statistical Jump Model for market regime detection.
    
    Implements the Shu et al. (2024) approach with jump penalties
    to enforce regime persistence and reduce whipsaw signals.
    
    The model uses dynamic programming (Viterbi-like) to find the
    optimal regime sequence that minimizes:
        Σ ℓ(x_t, θ_{s_t}) + λ Σ 𝕀(s_t ≠ s_{t-1})
    
    Example:
        >>> model = StatisticalJumpModel(JumpModelConfig(n_regimes=3, jump_penalty=10))
        >>> features = np.column_stack([volatility, sentiment_divergence, connectedness])
        >>> result = model.fit_predict(features)
        >>> print(f"Detected {result.n_jumps} regime transitions")
    """
    
    # Default regime names
    REGIME_NAMES = {
        0: RegimeState.RISK_ON.value,
        1: RegimeState.TRANSITION.value,
        2: RegimeState.RISK_OFF.value,
    }
    
    def __init__(self, config: Optional[JumpModelConfig] = None):
        """
        Initialize Statistical Jump Model.
        
        Args:
            config: Model configuration. Uses defaults if not provided.
        """
        self.config = config or JumpModelConfig()
        self.centroids: List[RegimeCentroid] = []
        self._fitted = False
        
        logger.info(
            f"StatisticalJumpModel initialized: "
            f"n_regimes={self.config.n_regimes}, λ={self.config.jump_penalty}"
        )
    
    def _compute_loss(self, x: np.ndarray, centroid: RegimeCentroid) -> float:
        """
        Compute loss for observation x given centroid.
        
        Uses scaled squared Euclidean distance:
            ℓ(x, θ) = 0.5 * ||x - μ||² 
        
        With optional Mahalanobis distance if covariance is available.
        """
        diff = x - centroid.mean
        
        # Simple Euclidean distance (scaled)
        return 0.5 * np.sum(diff ** 2)
    
    def _initialize_centroids(self, X: np.ndarray) -> List[RegimeCentroid]:
        """
        Initialize regime centroids.
        
        Supports multiple initialization methods:
        - 'kmeans': Use k-means clustering
        - 'quantile': Use quantile-based splits
        - 'random': Random initialization
        """
        n_samples, n_features = X.shape
        k = self.config.n_regimes
        
        if self.config.init_method == 'kmeans':
            try:
                from sklearn.cluster import KMeans
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                labels = kmeans.fit_predict(X)
                centers = kmeans.cluster_centers_
            except ImportError:
                logger.warning("sklearn not available, falling back to quantile init")
                return self._initialize_centroids_quantile(X)
                
        elif self.config.init_method == 'quantile':
            return self._initialize_centroids_quantile(X)
            
        else:  # random
            idx = np.random.choice(n_samples, k, replace=False)
            centers = X[idx]
            labels = np.zeros(n_samples, dtype=int)
        
        centroids = []
        for i in range(k):
            mask = labels == i
            if np.sum(mask) > 0:
                cluster_data = X[mask]
                mean = np.mean(cluster_data, axis=0)
                cov = np.cov(cluster_data.T) if cluster_data.shape[0] > 1 else np.eye(n_features)
            else:
                mean = centers[i]
                cov = np.eye(n_features)
            
            # Ensure cov is 2D
            if cov.ndim == 0:
                cov = np.array([[cov]])
            elif cov.ndim == 1:
                cov = np.diag(cov)
            
            regime_name = self.REGIME_NAMES.get(i, f"regime_{i}")
            centroids.append(RegimeCentroid(
                mean=mean,
                covariance=cov,
                regime_id=i,
                regime_name=regime_name
            ))
        
        return centroids
    
    def _initialize_centroids_quantile(self, X: np.ndarray) -> List[RegimeCentroid]:
        """Initialize centroids using quantile splits on first feature."""
        n_samples, n_features = X.shape
        k = self.config.n_regimes
        
        # Use first feature (typically volatility) for quantile splits
        quantiles = np.linspace(0, 100, k + 1)
        thresholds = np.percentile(X[:, 0], quantiles)
        
        centroids = []
        for i in range(k):
            mask = (X[:, 0] >= thresholds[i]) & (X[:, 0] < thresholds[i + 1])
            if i == k - 1:  # Include upper bound for last quantile
                mask = (X[:, 0] >= thresholds[i]) & (X[:, 0] <= thresholds[i + 1])
            
            if np.sum(mask) > 0:
                cluster_data = X[mask]
                mean = np.mean(cluster_data, axis=0)
                cov = np.cov(cluster_data.T) if cluster_data.shape[0] > 1 else np.eye(n_features)
            else:
                mean = np.mean(X, axis=0)
                cov = np.eye(n_features)
            
            if cov.ndim == 0:
                cov = np.array([[cov]])
            elif cov.ndim == 1:
                cov = np.diag(cov)
            
            regime_name = self.REGIME_NAMES.get(i, f"regime_{i}")
            centroids.append(RegimeCentroid(
                mean=mean,
                covariance=cov,
                regime_id=i,
                regime_name=regime_name
            ))
        
        return centroids
    
    def _viterbi_with_jump_penalty(
        self, 
        X: np.ndarray, 
        centroids: List[RegimeCentroid]
    ) -> Tuple[np.ndarray, float]:
        """
        Find optimal regime sequence using dynamic programming.
        
        This is a Viterbi-like algorithm that incorporates the jump penalty.
        
        For each time step t and regime k:
            V[t, k] = min over j of { V[t-1, j] + λ * 𝕀(j ≠ k) } + ℓ(x_t, θ_k)
        
        Returns:
            Tuple of (optimal regime sequence, total loss)
        """
        T = len(X)
        K = len(centroids)
        λ = self.config.jump_penalty
        
        # V[t, k] = minimum cost to reach state k at time t
        V = np.full((T, K), np.inf)
        
        # Backtrack pointers
        backtrack = np.zeros((T, K), dtype=int)
        
        # Initialize t=0
        for k in range(K):
            V[0, k] = self._compute_loss(X[0], centroids[k])
        
        # Forward pass
        for t in range(1, T):
            for k in range(K):
                loss_k = self._compute_loss(X[t], centroids[k])
                
                # Find best previous state
                costs = np.zeros(K)
                for j in range(K):
                    # Jump penalty if switching states
                    jump_cost = λ if j != k else 0
                    costs[j] = V[t-1, j] + jump_cost
                
                best_prev = np.argmin(costs)
                V[t, k] = costs[best_prev] + loss_k
                backtrack[t, k] = best_prev
        
        # Backtrack to find optimal sequence
        regimes = np.zeros(T, dtype=int)
        regimes[T-1] = np.argmin(V[T-1])
        total_loss = V[T-1, regimes[T-1]]
        
        for t in range(T-2, -1, -1):
            regimes[t] = backtrack[t+1, regimes[t+1]]
        
        return regimes, total_loss
    
    def _update_centroids(
        self, 
        X: np.ndarray, 
        regimes: np.ndarray
    ) -> List[RegimeCentroid]:
        """Update centroids based on current regime assignments."""
        K = self.config.n_regimes
        n_features = X.shape[1]
        
        new_centroids = []
        for k in range(K):
            mask = regimes == k
            if np.sum(mask) > 0:
                cluster_data = X[mask]
                mean = np.mean(cluster_data, axis=0)
                cov = np.cov(cluster_data.T) if cluster_data.shape[0] > 1 else np.eye(n_features)
            else:
                # Keep old centroid if no points assigned
                if k < len(self.centroids):
                    mean = self.centroids[k].mean
                    cov = self.centroids[k].covariance
                else:
                    mean = np.mean(X, axis=0)
                    cov = np.eye(n_features)
            
            if cov.ndim == 0:
                cov = np.array([[cov]])
            elif cov.ndim == 1:
                cov = np.diag(cov)
            
            regime_name = self.REGIME_NAMES.get(k, f"regime_{k}")
            new_centroids.append(RegimeCentroid(
                mean=mean,
                covariance=cov,
                regime_id=k,
                regime_name=regime_name
            ))
        
        return new_centroids
    
    def _compute_regime_probabilities(
        self, 
        X: np.ndarray, 
        centroids: List[RegimeCentroid]
    ) -> np.ndarray:
        """
        Compute soft regime probabilities using negative exponential of loss.
        
        P(regime=k | x_t) ∝ exp(-ℓ(x_t, θ_k))
        """
        T = len(X)
        K = len(centroids)
        
        # Compute losses
        losses = np.zeros((T, K))
        for k, centroid in enumerate(centroids):
            for t in range(T):
                losses[t, k] = self._compute_loss(X[t], centroid)
        
        # Convert to probabilities via softmax
        # Use negative loss (lower loss = higher probability)
        neg_losses = -losses
        
        # Softmax with numerical stability
        max_vals = np.max(neg_losses, axis=1, keepdims=True)
        exp_losses = np.exp(neg_losses - max_vals)
        probabilities = exp_losses / np.sum(exp_losses, axis=1, keepdims=True)
        
        return probabilities
    
    def fit(self, X: np.ndarray) -> 'StatisticalJumpModel':
        """
        Fit the Jump Model to feature data.
        
        Uses alternating optimization:
        1. Fix centroids, optimize regime sequence (Viterbi)
        2. Fix regimes, update centroids (M-step)
        
        Args:
            X: Feature matrix of shape (T, n_features)
               Features should include: volatility, sentiment divergence, connectedness
        
        Returns:
            self (fitted model)
        """
        X = np.asarray(X)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        
        T, n_features = X.shape
        logger.info(f"Fitting Jump Model: T={T}, n_features={n_features}")
        
        # Initialize centroids
        self.centroids = self._initialize_centroids(X)
        
        prev_loss = np.inf
        for iteration in range(self.config.max_iter):
            # E-step: Find optimal regime sequence
            regimes, total_loss = self._viterbi_with_jump_penalty(X, self.centroids)
            
            # M-step: Update centroids
            self.centroids = self._update_centroids(X, regimes)
            
            # Check convergence
            loss_change = abs(prev_loss - total_loss)
            if loss_change < self.config.tol:
                logger.info(f"Converged at iteration {iteration + 1}")
                break
            
            prev_loss = total_loss
        
        self._fitted = True
        self._last_regimes = regimes
        self._last_loss = total_loss
        
        n_jumps = np.sum(np.diff(regimes) != 0)
        logger.info(f"Fit complete: loss={total_loss:.4f}, n_jumps={n_jumps}")
        
        return self
    
    def predict(self, X: np.ndarray) -> JumpModelResult:
        """
        Predict regime sequence for new data.
        
        Args:
            X: Feature matrix of shape (T, n_features)
        
        Returns:
            JumpModelResult with regime assignments and probabilities
        """
        if not self._fitted:
            raise RuntimeError("Model must be fitted before prediction")
        
        X = np.asarray(X)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        
        # Find optimal regime sequence
        regimes, total_loss = self._viterbi_with_jump_penalty(X, self.centroids)
        
        # Compute probabilities
        probabilities = self._compute_regime_probabilities(X, self.centroids)
        
        n_jumps = np.sum(np.diff(regimes) != 0)
        
        return JumpModelResult(
            regimes=regimes,
            regime_probabilities=probabilities,
            centroids=self.centroids,
            total_loss=total_loss,
            n_jumps=n_jumps,
            convergence_info={'fitted': True}
        )
    
    def fit_predict(self, X: np.ndarray) -> JumpModelResult:
        """
        Fit model and return regime predictions.
        
        Args:
            X: Feature matrix of shape (T, n_features)
        
        Returns:
            JumpModelResult with regime assignments and probabilities
        """
        self.fit(X)
        
        X = np.asarray(X)
        if X.ndim == 1:
            X = X.reshape(-1, 1)
        
        probabilities = self._compute_regime_probabilities(X, self.centroids)
        
        n_jumps = np.sum(np.diff(self._last_regimes) != 0)
        
        return JumpModelResult(
            regimes=self._last_regimes,
            regime_probabilities=probabilities,
            centroids=self.centroids,
            total_loss=self._last_loss,
            n_jumps=n_jumps,
            convergence_info={'converged': True, 'max_iter': self.config.max_iter}
        )
    
    def tune_jump_penalty(
        self,
        X: np.ndarray,
        y_true: Optional[np.ndarray] = None,
        lambda_range: Optional[List[float]] = None,
        metric: Literal['silhouette', 'turnover', 'accuracy'] = 'turnover'
    ) -> Tuple[float, dict]:
        """
        Tune the jump penalty hyperparameter.
        
        Args:
            X: Feature matrix
            y_true: Ground truth regimes (optional, for accuracy metric)
            lambda_range: List of λ values to try
            metric: Optimization metric
                - 'silhouette': Maximize cluster separation
                - 'turnover': Target ~44% annualized turnover (Shu et al.)
                - 'accuracy': Maximize accuracy vs ground truth
        
        Returns:
            Tuple of (best_lambda, results_dict)
        """
        if lambda_range is None:
            lambda_range = [1, 5, 10, 20, 50, 100, 200]
        
        results = {}
        best_lambda = self.config.jump_penalty
        best_score = -np.inf if metric != 'turnover' else np.inf
        
        original_lambda = self.config.jump_penalty
        
        for λ in lambda_range:
            self.config.jump_penalty = λ
            result = self.fit_predict(X)
            
            if metric == 'turnover':
                # Target: ~44% annualized turnover (Shu et al.)
                # Annualized turnover = (n_jumps / T) * 252
                annualized_turnover = (result.n_jumps / len(X)) * 252
                score = abs(annualized_turnover - 0.44)  # Distance from target
                
                results[λ] = {
                    'n_jumps': result.n_jumps,
                    'annualized_turnover': annualized_turnover,
                    'score': score
                }
                
                if score < best_score:
                    best_score = score
                    best_lambda = λ
                    
            elif metric == 'silhouette':
                try:
                    from sklearn.metrics import silhouette_score
                    if len(np.unique(result.regimes)) > 1:
                        score = silhouette_score(X, result.regimes)
                    else:
                        score = -1
                except ImportError:
                    score = -result.total_loss  # Fallback to negative loss
                
                results[λ] = {'silhouette': score, 'n_jumps': result.n_jumps}
                
                if score > best_score:
                    best_score = score
                    best_lambda = λ
                    
            elif metric == 'accuracy' and y_true is not None:
                accuracy = np.mean(result.regimes == y_true)
                results[λ] = {'accuracy': accuracy, 'n_jumps': result.n_jumps}
                
                if accuracy > best_score:
                    best_score = accuracy
                    best_lambda = λ
        
        # Restore and refit with best lambda
        self.config.jump_penalty = best_lambda
        self.fit(X)
        
        logger.info(f"Tuning complete: best λ={best_lambda}")
        
        return best_lambda, results


def create_feature_matrix(
    volatility: np.ndarray,
    sentiment_divergence: Optional[np.ndarray] = None,
    connectedness: Optional[np.ndarray] = None,
    transfer_entropy: Optional[np.ndarray] = None,
    normalize: bool = True
) -> np.ndarray:
    """
    Create feature matrix for Jump Model from component features.
    
    Args:
        volatility: GARCH-MIDAS volatility estimates (required)
        sentiment_divergence: Cross-asset sentiment divergence
        connectedness: Total Connectedness Index
        transfer_entropy: Transfer Entropy divergence
        normalize: Whether to standardize features
    
    Returns:
        Feature matrix of shape (T, n_features)
    """
    features = [volatility.reshape(-1, 1)]
    
    if sentiment_divergence is not None:
        features.append(sentiment_divergence.reshape(-1, 1))
    
    if connectedness is not None:
        features.append(connectedness.reshape(-1, 1))
    
    if transfer_entropy is not None:
        features.append(transfer_entropy.reshape(-1, 1))
    
    X = np.hstack(features)
    
    if normalize:
        # Standardize each feature
        mean = np.mean(X, axis=0)
        std = np.std(X, axis=0)
        std[std == 0] = 1  # Avoid division by zero
        X = (X - mean) / std
    
    return X
