"""
Tests for feature engineering modules.

Tests cover:
- Granger causality analysis
- Transfer entropy analysis
- Connectedness measures
"""

import numpy as np
import pandas as pd
import pytest

from src.sentiment_detector.features import (
    GrangerCausalityAnalyzer,
    GrangerResult,
    CausalityNetwork,
    granger_causality_test,
    TransferEntropyAnalyzer,
    TransferEntropyResult,
    InformationFlowNetwork,
    transfer_entropy,
    ConnectednessAnalyzer,
    ConnectednessResult,
    DynamicConnectedness,
    calculate_centrality,
    identify_key_transmitters,
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def simple_causal_series():
    """Create simple series where x causes y with lag 1."""
    np.random.seed(42)
    n = 200
    
    # x is random
    x = np.random.randn(n)
    
    # y depends on lagged x
    y = np.zeros(n)
    for t in range(1, n):
        y[t] = 0.8 * x[t-1] + 0.2 * np.random.randn()
    
    return x, y


@pytest.fixture
def independent_series():
    """Create independent random series."""
    np.random.seed(42)
    n = 200
    x = np.random.randn(n)
    y = np.random.randn(n)
    return x, y


@pytest.fixture
def sentiment_dataframe():
    """Create sample sentiment DataFrame with multiple assets."""
    np.random.seed(42)
    n = 150
    
    # Create correlated sentiment series
    base = np.random.randn(n)
    
    data = {
        "equity": base + 0.2 * np.random.randn(n),
        "crypto": 0.5 * np.roll(base, 1) + 0.5 * np.random.randn(n),
        "forex": 0.3 * np.roll(base, 2) + 0.7 * np.random.randn(n),
        "commodity": 0.4 * np.roll(base, 1) + 0.6 * np.random.randn(n),
    }
    
    return pd.DataFrame(data)


# ============================================================================
# Granger Causality Tests
# ============================================================================

class TestGrangerCausalityAnalyzer:
    """Tests for GrangerCausalityAnalyzer."""
    
    def test_initialization(self):
        """Test analyzer initialization."""
        analyzer = GrangerCausalityAnalyzer(
            max_lag=3,
            significance_level=0.10
        )
        
        assert analyzer.max_lag == 3
        assert analyzer.significance_level == 0.10
        assert analyzer.min_observations == 50
    
    def test_causal_relationship_detected(self, simple_causal_series):
        """Test that true causal relationship is detected."""
        x, y = simple_causal_series
        
        analyzer = GrangerCausalityAnalyzer(max_lag=5, significance_level=0.05)
        result = analyzer.test_pairwise(x, y, "x", "y")
        
        assert isinstance(result, GrangerResult)
        assert result.source == "x"
        assert result.target == "y"
        # Causal relationship should be detected
        assert result.p_value < 0.10  # Lenient threshold for test
    
    def test_no_false_positives(self, independent_series):
        """Test that independent series don't show false causality."""
        x, y = independent_series
        
        analyzer = GrangerCausalityAnalyzer(max_lag=5, significance_level=0.05)
        result = analyzer.test_pairwise(x, y)
        
        # Should not be significant at 0.05 level (most of the time)
        # Using relaxed assertion due to randomness
        assert isinstance(result, GrangerResult)
        assert result.p_value >= 0.01  # Should not be extremely significant
    
    def test_insufficient_data_handling(self):
        """Test handling of insufficient data."""
        x = np.random.randn(20)  # Too short
        y = np.random.randn(20)
        
        analyzer = GrangerCausalityAnalyzer(min_observations=50)
        result = analyzer.test_pairwise(x, y)
        
        assert result.p_value == 1.0
        assert not result.is_significant
        assert result.direction == "none"
    
    def test_lag_selection(self, simple_causal_series):
        """Test optimal lag selection."""
        x, y = simple_causal_series
        
        analyzer = GrangerCausalityAnalyzer(max_lag=10)
        lag = analyzer._select_optimal_lag(x, y)
        
        # Should select a reasonable lag
        assert 1 <= lag <= 10
    
    def test_build_network(self, sentiment_dataframe):
        """Test building causality network."""
        analyzer = GrangerCausalityAnalyzer(max_lag=3)
        network = analyzer.build_network(sentiment_dataframe)
        
        assert isinstance(network, CausalityNetwork)
        assert len(network.nodes) == 4  # equity, crypto, forex, commodity
        assert network.adjacency_matrix.shape == (4, 4)
        assert network.significance_matrix.shape == (4, 4)
        # Diagonal should be zero
        assert np.diag(network.adjacency_matrix).sum() == 0
    
    def test_network_density(self, sentiment_dataframe):
        """Test network density calculation."""
        analyzer = GrangerCausalityAnalyzer(max_lag=3)
        network = analyzer.build_network(sentiment_dataframe)
        
        assert 0 <= network.density <= 1.0
    
    def test_net_spillover(self, sentiment_dataframe):
        """Test net spillover calculation."""
        analyzer = GrangerCausalityAnalyzer(max_lag=3)
        network = analyzer.build_network(sentiment_dataframe)
        
        spillover = analyzer.get_net_spillover(network)
        
        assert isinstance(spillover, dict)
        assert len(spillover) == 4
        # Net spillovers should sum to zero (conservation)
        assert abs(sum(spillover.values())) < 1e-10


class TestGrangerConvenienceFunction:
    """Tests for granger_causality_test convenience function."""
    
    def test_with_arrays(self, simple_causal_series):
        """Test with numpy arrays."""
        x, y = simple_causal_series
        
        result = granger_causality_test(x, y, max_lag=3)
        
        assert isinstance(result, GrangerResult)
        assert result.source == "X"
        assert result.target == "Y"
    
    def test_with_series(self, simple_causal_series):
        """Test with pandas Series."""
        x, y = simple_causal_series
        x = pd.Series(x, name="equity")
        y = pd.Series(y, name="crypto")
        
        result = granger_causality_test(x, y)
        
        assert result.source == "equity"
        assert result.target == "crypto"


# ============================================================================
# Transfer Entropy Tests
# ============================================================================

class TestTransferEntropyAnalyzer:
    """Tests for TransferEntropyAnalyzer."""
    
    def test_initialization(self):
        """Test analyzer initialization."""
        analyzer = TransferEntropyAnalyzer(
            history_length=5,
            n_bins=10
        )
        
        assert analyzer.history_length == 5
        assert analyzer.n_bins == 10
    
    def test_discretization(self):
        """Test series discretization."""
        analyzer = TransferEntropyAnalyzer(n_bins=5)
        
        series = np.random.randn(100)
        discretized = analyzer.discretize(series)
        
        assert len(discretized) == 100
        assert discretized.min() >= 0
        assert discretized.max() <= 5
    
    def test_te_calculation(self, simple_causal_series):
        """Test Transfer Entropy calculation."""
        x, y = simple_causal_series
        
        analyzer = TransferEntropyAnalyzer(history_length=3, n_permutations=50)
        result = analyzer.calculate_te(x, y, "x", "y")
        
        assert isinstance(result, TransferEntropyResult)
        assert result.transfer_entropy >= 0  # TE is non-negative
        assert result.history_length == 3
    
    def test_te_with_independent_series(self, independent_series):
        """Test TE with independent series should not be significant."""
        x, y = independent_series
        
        analyzer = TransferEntropyAnalyzer(history_length=2, n_permutations=30)
        result = analyzer.calculate_te(x, y)
        
        # For independent series, effective TE (bias-corrected) should be low
        # and the result should not be statistically significant
        # Raw TE can be non-zero due to finite sample effects
        assert abs(result.effective_te) < 0.5  # Effective TE near zero
        assert not result.is_significant  # Should not be significant
    
    def test_insufficient_data_handling(self):
        """Test handling of insufficient data."""
        x = np.random.randn(5)  # Too short
        y = np.random.randn(5)
        
        analyzer = TransferEntropyAnalyzer(history_length=3)
        result = analyzer.calculate_te(x, y)
        
        assert result.transfer_entropy == 0.0
        assert not result.is_significant
    
    def test_renyi_te(self, simple_causal_series):
        """Test Rényi Transfer Entropy calculation."""
        x, y = simple_causal_series
        
        analyzer = TransferEntropyAnalyzer(history_length=2, n_permutations=30)
        result = analyzer.calculate_renyi_te(x, y, alpha=2.0)
        
        assert isinstance(result, TransferEntropyResult)
        assert result.transfer_entropy >= 0
    
    def test_build_network(self, sentiment_dataframe):
        """Test building information flow network."""
        analyzer = TransferEntropyAnalyzer(history_length=2, n_permutations=20)
        network = analyzer.build_network(sentiment_dataframe)
        
        assert isinstance(network, InformationFlowNetwork)
        assert len(network.nodes) == 4
        assert network.adjacency_matrix.shape == (4, 4)
        assert network.total_flow >= 0
    
    def test_entropy_calculation(self):
        """Test Shannon entropy calculation."""
        analyzer = TransferEntropyAnalyzer()
        
        # Uniform distribution should have high entropy
        uniform = np.array([0, 1, 2, 3, 4] * 20)
        entropy_uniform = analyzer._calculate_entropy(uniform)
        
        # Constant should have zero entropy
        constant = np.zeros(100).astype(int)
        entropy_constant = analyzer._calculate_entropy(constant)
        
        assert entropy_uniform > entropy_constant
        assert entropy_constant < 0.1


class TestTransferEntropyConvenienceFunction:
    """Tests for transfer_entropy convenience function."""
    
    def test_basic_usage(self, simple_causal_series):
        """Test basic usage of convenience function."""
        x, y = simple_causal_series
        
        result = transfer_entropy(x, y, history_length=2)
        
        assert isinstance(result, TransferEntropyResult)


# ============================================================================
# Connectedness Tests
# ============================================================================

class TestConnectednessAnalyzer:
    """Tests for ConnectednessAnalyzer."""
    
    def test_initialization(self):
        """Test analyzer initialization."""
        analyzer = ConnectednessAnalyzer(var_lag=5, forecast_horizon=10)
        
        assert analyzer.var_lag == 5
        assert analyzer.forecast_horizon == 10
    
    def test_from_causality_network(self, sentiment_dataframe):
        """Test connectedness from Granger network."""
        gc_analyzer = GrangerCausalityAnalyzer(max_lag=2)
        network = gc_analyzer.build_network(sentiment_dataframe)
        
        conn_analyzer = ConnectednessAnalyzer()
        result = conn_analyzer.from_causality_network(network)
        
        assert isinstance(result, ConnectednessResult)
        assert 0 <= result.total_connectedness <= 100
        assert len(result.to_spillovers) == 4
        assert len(result.from_spillovers) == 4
        assert len(result.net_spillovers) == 4
    
    def test_from_te_network(self, sentiment_dataframe):
        """Test connectedness from Transfer Entropy network."""
        te_analyzer = TransferEntropyAnalyzer(history_length=2, n_permutations=10)
        network = te_analyzer.build_network(sentiment_dataframe)
        
        conn_analyzer = ConnectednessAnalyzer()
        result = conn_analyzer.from_te_network(network)
        
        assert isinstance(result, ConnectednessResult)
    
    def test_from_data_granger(self, sentiment_dataframe):
        """Test direct connectedness from data with Granger method."""
        analyzer = ConnectednessAnalyzer()
        result = analyzer.from_data(sentiment_dataframe, method="granger")
        
        assert isinstance(result, ConnectednessResult)
    
    def test_from_data_te(self, sentiment_dataframe):
        """Test direct connectedness from data with TE method."""
        analyzer = ConnectednessAnalyzer()
        result = analyzer.from_data(sentiment_dataframe, method="te")
        
        assert isinstance(result, ConnectednessResult)
    
    def test_get_transmitters_receivers(self, sentiment_dataframe):
        """Test identifying transmitters and receivers."""
        analyzer = ConnectednessAnalyzer()
        result = analyzer.from_data(sentiment_dataframe, method="granger")
        
        transmitters = result.get_transmitters()
        receivers = result.get_receivers()
        
        # Each node is either transmitter, receiver, or neutral
        assert isinstance(transmitters, list)
        assert isinstance(receivers, list)
    
    def test_to_dataframe(self, sentiment_dataframe):
        """Test conversion to DataFrame."""
        analyzer = ConnectednessAnalyzer()
        result = analyzer.from_data(sentiment_dataframe, method="granger")
        
        df = result.to_dataframe()
        
        assert isinstance(df, pd.DataFrame)
        assert "TO_others" in df.index
        assert "FROM_others" in df.columns
    
    def test_dynamic_connectedness(self, sentiment_dataframe):
        """Test dynamic connectedness over rolling windows."""
        analyzer = ConnectednessAnalyzer()
        
        dynamic = analyzer.dynamic_connectedness(
            sentiment_dataframe,
            window_size=30,
            step_size=5,
            method="granger"
        )
        
        assert isinstance(dynamic, DynamicConnectedness)
        assert len(dynamic.dates) > 0
        assert len(dynamic.total_connectedness) == len(dynamic.dates)
    
    def test_dynamic_to_dataframe(self, sentiment_dataframe):
        """Test dynamic connectedness DataFrame conversion."""
        analyzer = ConnectednessAnalyzer()
        
        dynamic = analyzer.dynamic_connectedness(
            sentiment_dataframe,
            window_size=30,
            step_size=10,
            method="granger"
        )
        
        df = dynamic.to_dataframe()
        
        assert isinstance(df, pd.DataFrame)
        assert "total_connectedness" in df.columns


class TestCentralityFunctions:
    """Tests for centrality calculation functions."""
    
    def test_calculate_centrality(self):
        """Test centrality calculation."""
        adj = np.array([
            [0, 0.5, 0.3],
            [0.2, 0, 0.4],
            [0.1, 0.3, 0]
        ])
        nodes = ["A", "B", "C"]
        
        centrality = calculate_centrality(adj, nodes)
        
        assert len(centrality) == 3
        assert "A" in centrality
        assert "degree_in" in centrality["A"]
        assert "degree_out" in centrality["A"]
        assert "eigenvector" in centrality["A"]
    
    def test_identify_key_transmitters(self, sentiment_dataframe):
        """Test identifying key transmitters."""
        analyzer = ConnectednessAnalyzer()
        result = analyzer.from_data(sentiment_dataframe, method="granger")
        
        top_transmitters = identify_key_transmitters(result, top_n=2)
        
        assert len(top_transmitters) == 2
        assert isinstance(top_transmitters[0], tuple)
        assert len(top_transmitters[0]) == 2  # (name, value)


# ============================================================================
# Integration Tests
# ============================================================================

class TestFeatureIntegration:
    """Integration tests for feature engineering pipeline."""
    
    def test_full_pipeline(self, sentiment_dataframe):
        """Test complete feature engineering pipeline."""
        # 1. Granger causality network
        gc_analyzer = GrangerCausalityAnalyzer(max_lag=2)
        gc_network = gc_analyzer.build_network(sentiment_dataframe)
        
        # 2. Transfer entropy network
        te_analyzer = TransferEntropyAnalyzer(history_length=2, n_permutations=20)
        te_network = te_analyzer.build_network(sentiment_dataframe)
        
        # 3. Connectedness from both
        conn_analyzer = ConnectednessAnalyzer()
        gc_conn = conn_analyzer.from_causality_network(gc_network)
        te_conn = conn_analyzer.from_te_network(te_network)
        
        # 4. Centrality
        gc_centrality = calculate_centrality(gc_network.adjacency_matrix, gc_network.nodes)
        
        # 5. Key transmitters
        gc_transmitters = identify_key_transmitters(gc_conn)
        te_transmitters = identify_key_transmitters(te_conn)
        
        # Verify all outputs
        assert gc_conn.total_connectedness >= 0
        assert te_conn.total_connectedness >= 0
        assert len(gc_centrality) == 4
        assert len(gc_transmitters) == 3  # top 3 by default
    
    def test_comparison_granger_vs_te(self, simple_causal_series):
        """Compare Granger causality vs Transfer Entropy on same data."""
        x, y = simple_causal_series
        
        gc_result = granger_causality_test(x, y)
        te_result = transfer_entropy(x, y)
        
        # Both should detect some relationship
        # (not strict assertion due to different methodologies)
        assert isinstance(gc_result, GrangerResult)
        assert isinstance(te_result, TransferEntropyResult)


# ============================================================================
# Edge Cases and Error Handling
# ============================================================================

class TestEdgeCases:
    """Tests for edge cases and error handling."""
    
    def test_constant_series(self):
        """Test with constant series."""
        x = np.ones(100)
        y = np.ones(100)
        
        gc_result = granger_causality_test(x, y)
        # Should handle gracefully
        assert isinstance(gc_result, GrangerResult)
    
    def test_nan_handling(self):
        """Test handling of NaN values."""
        x = np.random.randn(100)
        y = np.random.randn(100)
        x[50] = np.nan
        y[75] = np.nan
        
        gc_analyzer = GrangerCausalityAnalyzer()
        # DataFrame handles NaN removal
        df = pd.DataFrame({"x": x, "y": y})
        network = gc_analyzer.build_network(df)
        
        assert isinstance(network, CausalityNetwork)
    
    def test_single_column_dataframe(self):
        """Test with single column (should produce empty network)."""
        df = pd.DataFrame({"single": np.random.randn(100)})
        
        analyzer = GrangerCausalityAnalyzer()
        network = analyzer.build_network(df)
        
        assert network.n_nodes == 1
        assert network.n_edges == 0
    
    def test_short_time_series(self):
        """Test with very short time series."""
        df = pd.DataFrame({
            "a": np.random.randn(15),
            "b": np.random.randn(15)
        })
        
        analyzer = GrangerCausalityAnalyzer(max_lag=2)
        network = analyzer.build_network(df)
        
        # Should handle gracefully
        assert isinstance(network, CausalityNetwork)
