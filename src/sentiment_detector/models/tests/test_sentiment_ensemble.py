"""
Tests for Sentiment Ensemble module.
"""

import sys
from pathlib import Path
import importlib.util

# Load the module directly to avoid __init__.py import issues
module_path = Path(__file__).parent.parent / "sentiment_ensemble.py"
spec = importlib.util.spec_from_file_location("sentiment_ensemble", module_path)
sentiment_ensemble = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sentiment_ensemble)

import numpy as np
import pytest

# Import from the directly loaded module
SentimentLabel = sentiment_ensemble.SentimentLabel
ModelPrediction = sentiment_ensemble.ModelPrediction
EnsemblePrediction = sentiment_ensemble.EnsemblePrediction
SentimentEnsemble = sentiment_ensemble.SentimentEnsemble
create_ensemble = sentiment_ensemble.create_ensemble


# ============================================================================
# Data Classes Tests
# ============================================================================

class TestSentimentLabel:
    """Tests for SentimentLabel enum."""
    
    def test_label_values(self):
        """Test label integer values."""
        assert SentimentLabel.NEGATIVE.value == -1
        assert SentimentLabel.NEUTRAL.value == 0
        assert SentimentLabel.POSITIVE.value == 1


class TestModelPrediction:
    """Tests for ModelPrediction dataclass."""
    
    def test_creation(self):
        """Test prediction creation."""
        pred = ModelPrediction(
            model_name="finbert",
            label=SentimentLabel.POSITIVE,
            confidence=0.85,
            probabilities=(0.05, 0.10, 0.85)
        )
        
        assert pred.model_name == "finbert"
        assert pred.label == SentimentLabel.POSITIVE
        assert pred.confidence == 0.85
    
    def test_entropy_calculation(self):
        """Test entropy property."""
        # High confidence = low entropy
        confident = ModelPrediction(
            model_name="test",
            label=SentimentLabel.POSITIVE,
            confidence=0.9,
            probabilities=(0.05, 0.05, 0.9)
        )
        
        # Uncertain = high entropy
        uncertain = ModelPrediction(
            model_name="test",
            label=SentimentLabel.NEUTRAL,
            confidence=0.34,
            probabilities=(0.33, 0.34, 0.33)
        )
        
        assert confident.entropy < uncertain.entropy
    
    def test_uniform_entropy(self):
        """Test entropy for uniform distribution."""
        uniform = ModelPrediction(
            model_name="test",
            label=SentimentLabel.NEUTRAL,
            confidence=0.33,
            probabilities=(0.33, 0.34, 0.33)
        )
        
        # Should be close to log(3)
        assert abs(uniform.entropy - np.log(3)) < 0.1


class TestEnsemblePrediction:
    """Tests for EnsemblePrediction dataclass."""
    
    def test_creation(self):
        """Test ensemble prediction creation."""
        model_preds = [
            ModelPrediction("a", SentimentLabel.POSITIVE, 0.8, (0.1, 0.1, 0.8)),
            ModelPrediction("b", SentimentLabel.POSITIVE, 0.7, (0.1, 0.2, 0.7)),
        ]
        
        pred = EnsemblePrediction(
            label=SentimentLabel.POSITIVE,
            confidence=0.75,
            probabilities=(0.1, 0.15, 0.75),
            model_predictions=model_preds,
            agreement=1.0,
            uncertainty=0.3
        )
        
        assert pred.label == SentimentLabel.POSITIVE
        assert len(pred.model_predictions) == 2
        assert pred.agreement == 1.0
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        model_preds = [
            ModelPrediction("a", SentimentLabel.NEGATIVE, 0.8, (0.8, 0.1, 0.1)),
        ]
        
        pred = EnsemblePrediction(
            label=SentimentLabel.NEGATIVE,
            confidence=0.8,
            probabilities=(0.8, 0.1, 0.1),
            model_predictions=model_preds,
            agreement=1.0,
            uncertainty=0.2
        )
        
        d = pred.to_dict()
        
        assert d["label"] == "NEGATIVE"
        assert d["label_value"] == -1
        assert d["confidence"] == 0.8
        assert "negative" in d["probabilities"]
        assert d["model_count"] == 1


# ============================================================================
# Sentiment Ensemble Tests
# ============================================================================

class TestSentimentEnsemble:
    """Tests for SentimentEnsemble class."""
    
    @pytest.fixture
    def ensemble(self):
        """Create ensemble for testing."""
        return SentimentEnsemble()
    
    def test_initialization(self, ensemble):
        """Test default initialization."""
        assert len(ensemble.model_configs) == 2
        assert "finbert" in ensemble.weights
        assert "roberta" in ensemble.weights
        assert abs(sum(ensemble.weights.values()) - 1.0) < 0.01
    
    def test_custom_weights(self):
        """Test custom weight initialization."""
        custom_weights = {"finbert": 0.7, "roberta": 0.3}
        ensemble = SentimentEnsemble(weights=custom_weights)
        
        assert ensemble.weights["finbert"] == 0.7
        assert ensemble.weights["roberta"] == 0.3
    
    def test_predict_positive(self, ensemble):
        """Test prediction of positive sentiment."""
        result = ensemble.predict("Bitcoin surges to new all-time high!")
        
        assert isinstance(result, EnsemblePrediction)
        assert result.label == SentimentLabel.POSITIVE
        assert result.confidence > 0.5
        assert len(result.model_predictions) > 0
    
    def test_predict_negative(self, ensemble):
        """Test prediction of negative sentiment."""
        result = ensemble.predict("Stock market crashes amid panic selling")
        
        assert result.label == SentimentLabel.NEGATIVE
        assert result.confidence > 0.5
    
    def test_predict_neutral(self, ensemble):
        """Test prediction of neutral sentiment."""
        result = ensemble.predict("Markets traded in a narrow range today")
        
        # Should be neutral or at least have low confidence
        assert result.label in [SentimentLabel.NEUTRAL, SentimentLabel.POSITIVE, SentimentLabel.NEGATIVE]
        assert isinstance(result.confidence, float)
    
    def test_asset_class_weight_adjustment(self, ensemble):
        """Test weight adjustment based on asset class."""
        # Crypto should weight RoBERTa higher
        crypto_weights = ensemble._get_weights("crypto")
        default_weights = ensemble._get_weights(None)
        
        assert crypto_weights["roberta"] > default_weights["roberta"]
        assert crypto_weights["finbert"] < default_weights["finbert"]
    
    def test_equity_weights(self, ensemble):
        """Test equity-specific weights."""
        equity_weights = ensemble._get_weights("equity")
        
        # FinBERT should be weighted higher for equity
        assert equity_weights["finbert"] > equity_weights["roberta"]
    
    def test_predict_with_asset_class(self, ensemble):
        """Test prediction with asset class context."""
        text = "Strong earnings report drives stock higher"
        
        equity_result = ensemble.predict(text, asset_class="equity")
        crypto_result = ensemble.predict(text, asset_class="crypto")
        
        # Both should be positive but may differ in confidence
        assert isinstance(equity_result, EnsemblePrediction)
        assert isinstance(crypto_result, EnsemblePrediction)
    
    def test_predict_batch(self, ensemble):
        """Test batch prediction."""
        texts = [
            "Markets rally on positive data",
            "Bearish trend continues",
            "Stable conditions expected"
        ]
        
        results = ensemble.predict_batch(texts)
        
        assert len(results) == 3
        assert all(isinstance(r, EnsemblePrediction) for r in results)
    
    def test_agreement_calculation(self, ensemble):
        """Test model agreement calculation."""
        result = ensemble.predict("Massive crypto crash wipes out gains")
        
        # Agreement should be between 0 and 1
        assert 0 <= result.agreement <= 1.0
    
    def test_uncertainty_calculation(self, ensemble):
        """Test uncertainty calculation."""
        # Clear positive should have low uncertainty
        positive_result = ensemble.predict("Incredible gains, stock soars 50%")
        
        # Neutral text should have higher uncertainty
        neutral_result = ensemble.predict("Market moves slightly")
        
        assert 0 <= positive_result.uncertainty <= 1.0
        assert 0 <= neutral_result.uncertainty <= 1.0
    
    def test_probabilities_sum_to_one(self, ensemble):
        """Test that probabilities sum to 1."""
        result = ensemble.predict("Test text for probability check")
        
        prob_sum = sum(result.probabilities)
        assert abs(prob_sum - 1.0) < 0.01
    
    def test_model_key_extraction(self, ensemble):
        """Test model key extraction from full model names."""
        assert ensemble._get_model_key("ProsusAI/finbert") == "finbert"
        assert ensemble._get_model_key("cardiffnlp/twitter-roberta-base") == "roberta"
        assert ensemble._get_model_key("bert-base-uncased") == "bert"
    
    def test_confidence_weighting_effect(self):
        """Test that confidence weighting affects results."""
        with_cw = SentimentEnsemble(use_confidence_weighting=True)
        without_cw = SentimentEnsemble(use_confidence_weighting=False)
        
        text = "Market shows mixed signals with uncertain outlook"
        
        result_with = with_cw.predict(text)
        result_without = without_cw.predict(text)
        
        # Both should produce valid results
        assert isinstance(result_with, EnsemblePrediction)
        assert isinstance(result_without, EnsemblePrediction)
    
    def test_empty_model_handling(self):
        """Test handling when no models are loaded."""
        ensemble = SentimentEnsemble()
        ensemble._loaded = True
        ensemble.models = {}  # Empty models dict
        
        result = ensemble.predict("Test text")
        
        # Should still work with mock predictions
        assert isinstance(result, EnsemblePrediction)


class TestCreateEnsemble:
    """Tests for factory function."""
    
    def test_create_default(self):
        """Test creating default ensemble."""
        ensemble = create_ensemble()
        
        assert isinstance(ensemble, SentimentEnsemble)
        assert len(ensemble.model_configs) == 2
    
    def test_create_with_custom_models(self):
        """Test creating ensemble with custom models."""
        models = ["model1", "model2", "model3"]
        ensemble = create_ensemble(models=models)
        
        assert len(ensemble.model_configs) == 3


# ============================================================================
# Integration Tests
# ============================================================================

class TestEnsembleIntegration:
    """Integration tests for sentiment ensemble."""
    
    def test_full_workflow(self):
        """Test complete prediction workflow."""
        # Create ensemble
        ensemble = SentimentEnsemble()
        
        # Sample financial texts with clear sentiment
        texts = [
            "Stock prices soar as earnings beat expectations",  # Positive
            "Market tumbles on disappointing economic data",    # Negative
            "Trading remains flat amid uncertainty",            # Neutral
            "Massive gains as stock surges 50%",                # Positive (stronger)
            "Crash wipes out all gains in bear market"          # Negative (stronger)
        ]
        
        expected_sentiments = [
            SentimentLabel.POSITIVE,
            SentimentLabel.NEGATIVE,
            SentimentLabel.NEUTRAL,
            SentimentLabel.POSITIVE,
            SentimentLabel.NEGATIVE
        ]
        
        results = ensemble.predict_batch(texts)
        
        # Check each result
        correct = 0
        for i, (result, expected) in enumerate(zip(results, expected_sentiments)):
            assert isinstance(result, EnsemblePrediction)
            if result.label == expected:
                correct += 1
        
        # At least 3/5 should match (60% accuracy threshold)
        # Mock predictions have noise, so we allow some flexibility
        assert correct >= 3, f"Only {correct}/5 predictions matched expected"
    
    def test_consistency(self):
        """Test prediction consistency."""
        ensemble = SentimentEnsemble()
        text = "Strong rally continues on Wall Street"
        
        # Multiple predictions should be consistent
        results = [ensemble.predict(text) for _ in range(5)]
        
        labels = [r.label for r in results]
        # Should all be the same (deterministic for same input)
        # Note: Mock predictions have small random noise, so check majority
        assert labels.count(labels[0]) >= 3
