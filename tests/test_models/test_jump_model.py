"""
Tests for Statistical Jump Model.

Tests the Shu et al. (2024) Jump Model implementation including:
- Initialization methods
- Viterbi optimization with jump penalty
- Centroid updates
- Hyperparameter tuning
"""

import pytest
import numpy as np
from datetime import datetime

from sentiment_detector.models.jump_model import (
    StatisticalJumpModel,
    JumpModelConfig,
    JumpModelResult,
    RegimeCentroid,
    RegimeState,
    create_feature_matrix,
)


class TestJumpModelConfig:
    """Tests for JumpModelConfig."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = JumpModelConfig()
        assert config.n_regimes == 3
        assert config.jump_penalty == 10.0
        assert config.max_iter == 100
        assert config.init_method == 'kmeans'
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = JumpModelConfig(
            n_regimes=2,
            jump_penalty=50.0,
            init_method='quantile'
        )
        assert config.n_regimes == 2
        assert config.jump_penalty == 50.0
        assert config.init_method == 'quantile'


class TestStatisticalJumpModel:
    """Tests for StatisticalJumpModel."""
    
    @pytest.fixture
    def simple_data(self):
        """Generate simple test data with clear regimes."""
        np.random.seed(42)
        
        # Three regimes with distinct means
        regime_0 = np.random.randn(50, 2) + [0, 0]  # Risk-on (low vol)
        regime_1 = np.random.randn(30, 2) + [2, 1]  # Transition
        regime_2 = np.random.randn(50, 2) + [4, 2]  # Risk-off (high vol)
        regime_0b = np.random.randn(30, 2) + [0, 0]  # Back to risk-on
        
        X = np.vstack([regime_0, regime_1, regime_2, regime_0b])
        y_true = np.concatenate([
            np.zeros(50, dtype=int),
            np.ones(30, dtype=int),
            np.full(50, 2, dtype=int),
            np.zeros(30, dtype=int)
        ])
        
        return X, y_true
    
    @pytest.fixture
    def model(self):
        """Create a default model."""
        return StatisticalJumpModel(JumpModelConfig(n_regimes=3, jump_penalty=10.0))
    
    def test_initialization(self):
        """Test model initialization."""
        model = StatisticalJumpModel()
        assert model.config.n_regimes == 3
        assert not model._fitted
    
    def test_fit_basic(self, model, simple_data):
        """Test basic fitting."""
        X, _ = simple_data
        model.fit(X)
        
        assert model._fitted
        assert len(model.centroids) == 3
        assert model._last_loss is not None
    
    def test_fit_predict(self, model, simple_data):
        """Test fit_predict returns valid result."""
        X, y_true = simple_data
        result = model.fit_predict(X)
        
        assert isinstance(result, JumpModelResult)
        assert len(result.regimes) == len(X)
        assert result.regime_probabilities.shape == (len(X), 3)
        assert result.n_jumps >= 0
        assert result.total_loss > 0
    
    def test_regime_persistence(self, simple_data):
        """Test that higher jump penalty reduces transitions."""
        X, _ = simple_data
        
        # Low penalty
        model_low = StatisticalJumpModel(JumpModelConfig(jump_penalty=1.0))
        result_low = model_low.fit_predict(X)
        
        # High penalty
        model_high = StatisticalJumpModel(JumpModelConfig(jump_penalty=100.0))
        result_high = model_high.fit_predict(X)
        
        # Higher penalty should have fewer jumps
        assert result_high.n_jumps <= result_low.n_jumps
    
    def test_predict_requires_fit(self, model, simple_data):
        """Test that predict raises error if not fitted."""
        X, _ = simple_data
        with pytest.raises(RuntimeError, match="must be fitted"):
            model.predict(X)
    
    def test_regime_names(self, model, simple_data):
        """Test regime name mapping."""
        X, _ = simple_data
        result = model.fit_predict(X)
        
        names = result.regime_names
        assert len(names) == len(X)
        assert all(n in ['risk_on', 'transition', 'risk_off'] for n in names)
    
    def test_regime_durations(self, model, simple_data):
        """Test regime duration calculation."""
        X, _ = simple_data
        result = model.fit_predict(X)
        
        durations = result.get_regime_durations()
        assert isinstance(durations, dict)
        # At least one regime should have positive duration
        assert any(d > 0 for d in durations.values())
    
    def test_probabilities_sum_to_one(self, model, simple_data):
        """Test that regime probabilities sum to 1."""
        X, _ = simple_data
        result = model.fit_predict(X)
        
        prob_sums = np.sum(result.regime_probabilities, axis=1)
        np.testing.assert_array_almost_equal(prob_sums, np.ones(len(X)))
    
    def test_1d_input(self, model):
        """Test handling of 1D input."""
        X = np.random.randn(100)
        result = model.fit_predict(X)
        
        assert len(result.regimes) == 100
    
    def test_quantile_initialization(self, simple_data):
        """Test quantile-based initialization."""
        X, _ = simple_data
        model = StatisticalJumpModel(JumpModelConfig(init_method='quantile'))
        result = model.fit_predict(X)
        
        assert len(result.regimes) == len(X)


class TestJumpPenaltyTuning:
    """Tests for hyperparameter tuning."""
    
    @pytest.fixture
    def data(self):
        """Generate test data."""
        np.random.seed(42)
        X = np.vstack([
            np.random.randn(100, 2) + [0, 0],
            np.random.randn(100, 2) + [3, 2],
        ])
        return X
    
    def test_tune_turnover(self, data):
        """Test tuning with turnover metric."""
        model = StatisticalJumpModel()
        best_lambda, results = model.tune_jump_penalty(
            data,
            lambda_range=[5, 10, 20],
            metric='turnover'
        )
        
        assert best_lambda in [5, 10, 20]
        assert len(results) == 3
        assert all('n_jumps' in r for r in results.values())
    
    def test_tune_silhouette(self, data):
        """Test tuning with silhouette metric."""
        model = StatisticalJumpModel()
        best_lambda, results = model.tune_jump_penalty(
            data,
            lambda_range=[5, 10, 20],
            metric='silhouette'
        )
        
        assert best_lambda in [5, 10, 20]


class TestFeatureMatrix:
    """Tests for create_feature_matrix."""
    
    def test_volatility_only(self):
        """Test with only volatility."""
        vol = np.random.rand(100)
        X = create_feature_matrix(vol)
        
        assert X.shape == (100, 1)
    
    def test_all_features(self):
        """Test with all features."""
        n = 100
        X = create_feature_matrix(
            volatility=np.random.rand(n),
            sentiment_divergence=np.random.rand(n),
            connectedness=np.random.rand(n),
            transfer_entropy=np.random.rand(n)
        )
        
        assert X.shape == (n, 4)
    
    def test_normalization(self):
        """Test that normalization produces zero mean, unit variance."""
        vol = np.random.rand(100) * 10 + 5
        X = create_feature_matrix(vol, normalize=True)
        
        np.testing.assert_almost_equal(np.mean(X), 0, decimal=10)
        np.testing.assert_almost_equal(np.std(X), 1, decimal=10)
    
    def test_no_normalization(self):
        """Test without normalization."""
        vol = np.random.rand(100) * 10 + 5
        X = create_feature_matrix(vol, normalize=False)
        
        # Should not be standardized
        assert np.mean(X) > 1


class TestRegimeCentroid:
    """Tests for RegimeCentroid dataclass."""
    
    def test_n_features(self):
        """Test n_features property."""
        centroid = RegimeCentroid(
            mean=np.array([1.0, 2.0, 3.0]),
            covariance=np.eye(3),
            regime_id=0,
            regime_name='test'
        )
        assert centroid.n_features == 3


class TestIntegrationWithGARCHMIDAS:
    """Integration tests with GARCH-MIDAS output."""
    
    def test_full_pipeline(self):
        """Test Jump Model with simulated GARCH-MIDAS output."""
        np.random.seed(42)
        T = 252  # One year of trading days
        
        # Simulate GARCH-MIDAS volatility (3 regimes)
        volatility = np.concatenate([
            0.1 + 0.02 * np.random.randn(80),   # Low vol
            0.25 + 0.05 * np.random.randn(80),  # Normal
            0.4 + 0.08 * np.random.randn(92),   # High vol
        ])
        
        # Simulate sentiment divergence
        divergence = np.concatenate([
            0.1 * np.random.randn(80),
            0.2 * np.random.randn(80),
            0.5 + 0.3 * np.random.randn(92),
        ])
        
        # Create feature matrix
        X = create_feature_matrix(
            volatility=volatility,
            sentiment_divergence=divergence
        )
        
        # Fit Jump Model
        config = JumpModelConfig(n_regimes=3, jump_penalty=20.0)
        model = StatisticalJumpModel(config)
        result = model.fit_predict(X)
        
        # Validate result
        assert len(result.regimes) == T
        assert result.n_jumps >= 1  # At least 1 transition expected
        assert result.n_jumps < T // 2  # But not too many
        
        # Check regime durations are reasonable
        durations = result.get_regime_durations()
        # At least some regimes should have non-zero duration
        assert sum(d > 0 for d in durations.values()) >= 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
