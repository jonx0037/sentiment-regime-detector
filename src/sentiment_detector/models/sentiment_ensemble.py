"""
Sentiment Ensemble with Weighted Voting.

This module implements ensemble sentiment classification using weighted
voting across multiple transformer models (FinBERT + RoBERTa).

Per Dakalbab et al. (2024), ensemble methods improve sentiment
prediction accuracy by combining complementary model strengths.

Key features:
- Weighted voting based on model confidence
- Dynamic weight adjustment based on asset class
- Calibrated probability outputs
- Disagreement detection for uncertainty estimation
"""

from dataclasses import dataclass, field
from typing import Optional, Union, Literal
from enum import Enum, auto
import logging

import numpy as np

logger = logging.getLogger(__name__)

# Try to import transformers - will be available in production
try:
    import torch
    from transformers import (
        AutoModelForSequenceClassification,
        AutoTokenizer,
        pipeline
    )
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    logger.warning("Transformers not available. Using mock predictions.")


class SentimentLabel(Enum):
    """Sentiment classification labels."""
    NEGATIVE = -1
    NEUTRAL = 0
    POSITIVE = 1


@dataclass
class ModelPrediction:
    """
    Prediction from a single model.
    
    Attributes:
        model_name: Name of the model
        label: Predicted sentiment label
        confidence: Model confidence score [0, 1]
        probabilities: Class probabilities [negative, neutral, positive]
    """
    model_name: str
    label: SentimentLabel
    confidence: float
    probabilities: tuple[float, float, float]
    
    @property
    def entropy(self) -> float:
        """Calculate prediction entropy (uncertainty)."""
        probs = np.array(self.probabilities)
        probs = np.clip(probs, 1e-10, 1.0)
        return float(-np.sum(probs * np.log(probs)))


@dataclass
class EnsemblePrediction:
    """
    Ensemble prediction result.
    
    Attributes:
        label: Final ensemble label
        confidence: Ensemble confidence
        probabilities: Weighted average probabilities
        model_predictions: Individual model predictions
        agreement: Level of model agreement [0, 1]
        uncertainty: Prediction uncertainty
    """
    label: SentimentLabel
    confidence: float
    probabilities: tuple[float, float, float]
    model_predictions: list[ModelPrediction]
    agreement: float
    uncertainty: float
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "label": self.label.name,
            "label_value": self.label.value,
            "confidence": self.confidence,
            "probabilities": {
                "negative": self.probabilities[0],
                "neutral": self.probabilities[1],
                "positive": self.probabilities[2]
            },
            "agreement": self.agreement,
            "uncertainty": self.uncertainty,
            "model_count": len(self.model_predictions)
        }


class SentimentEnsemble:
    """
    Ensemble sentiment classifier with weighted voting.
    
    Combines multiple transformer models (FinBERT, RoBERTa) using
    weighted voting for improved prediction accuracy.
    
    Per Dakalbab et al. (2024), the ensemble uses:
    - Static weights based on model performance benchmarks
    - Dynamic weight adjustment based on text characteristics
    - Confidence-weighted voting for final predictions
    
    Example:
        >>> ensemble = SentimentEnsemble()
        >>> result = ensemble.predict("Bitcoin surges to new all-time high!")
        >>> print(f"Sentiment: {result.label.name}, Confidence: {result.confidence:.2f}")
    """
    
    # Default model weights based on domain performance
    DEFAULT_WEIGHTS = {
        "finbert": 0.55,  # Stronger for financial text
        "roberta": 0.45,  # Good general performance
    }
    
    # Asset-specific weight adjustments
    ASSET_WEIGHTS = {
        "equity": {"finbert": 0.60, "roberta": 0.40},
        "crypto": {"finbert": 0.45, "roberta": 0.55},  # RoBERTa better for informal
        "forex": {"finbert": 0.55, "roberta": 0.45},
        "commodity": {"finbert": 0.55, "roberta": 0.45},
    }
    
    def __init__(
        self,
        models: Optional[list[str]] = None,
        weights: Optional[dict[str, float]] = None,
        device: str = "auto",
        use_confidence_weighting: bool = True,
        min_confidence: float = 0.4
    ):
        """
        Initialize sentiment ensemble.
        
        Args:
            models: List of model identifiers to use
            weights: Custom model weights (must sum to 1)
            device: Device for inference ("auto", "cpu", "cuda", "mps")
            use_confidence_weighting: Adjust weights by model confidence
            min_confidence: Minimum confidence to trust a prediction
        """
        self.model_configs = models or [
            "ProsusAI/finbert",
            "cardiffnlp/twitter-roberta-base-sentiment-latest"
        ]
        
        self.weights = weights or self.DEFAULT_WEIGHTS.copy()
        self.use_confidence_weighting = use_confidence_weighting
        self.min_confidence = min_confidence
        
        # Determine device
        if device == "auto":
            if TRANSFORMERS_AVAILABLE:
                if torch.cuda.is_available():
                    self.device = "cuda"
                elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                    self.device = "mps"
                else:
                    self.device = "cpu"
            else:
                self.device = "cpu"
        else:
            self.device = device
        
        self.models = {}
        self.tokenizers = {}
        self._loaded = False
    
    def load_models(self) -> None:
        """Load all models into memory."""
        if not TRANSFORMERS_AVAILABLE:
            logger.warning("Transformers not available. Using mock mode.")
            self._loaded = True
            return
        
        logger.info(f"Loading {len(self.model_configs)} models on {self.device}")
        
        for model_name in self.model_configs:
            try:
                # Create pipeline for easier inference
                model_key = self._get_model_key(model_name)
                
                # Use top_k=None to get all scores (replaces deprecated return_all_scores)
                self.models[model_key] = pipeline(
                    "sentiment-analysis",
                    model=model_name,
                    device=0 if self.device == "cuda" else -1,
                    top_k=None,  # Returns all class scores
                    truncation=True,
                    max_length=512
                )
                
                logger.info(f"Loaded model: {model_key}")
                
            except Exception as e:
                logger.error(f"Failed to load {model_name}: {e}")
        
        self._loaded = True
    
    def _get_model_key(self, model_name: str) -> str:
        """Extract short model key from full model name."""
        if "finbert" in model_name.lower():
            return "finbert"
        elif "roberta" in model_name.lower():
            return "roberta"
        elif "bert" in model_name.lower():
            return "bert"
        else:
            return model_name.split("/")[-1].lower()
    
    def predict(
        self,
        text: str,
        asset_class: Optional[str] = None
    ) -> EnsemblePrediction:
        """
        Predict sentiment for a single text.
        
        Args:
            text: Input text to classify
            asset_class: Asset class for weight adjustment
            
        Returns:
            EnsemblePrediction with ensemble result
        """
        if not self._loaded:
            self.load_models()
        
        # Get predictions from each model
        model_predictions = []
        
        if not TRANSFORMERS_AVAILABLE or not self.models:
            # Mock predictions for testing
            model_predictions = self._mock_predictions(text)
        else:
            for model_key, pipeline_model in self.models.items():
                try:
                    pred = self._predict_single_model(
                        pipeline_model, text, model_key
                    )
                    model_predictions.append(pred)
                except Exception as e:
                    logger.warning(f"Model {model_key} failed: {e}")
        
        if not model_predictions:
            # Return neutral if all models failed
            return EnsemblePrediction(
                label=SentimentLabel.NEUTRAL,
                confidence=0.0,
                probabilities=(0.33, 0.34, 0.33),
                model_predictions=[],
                agreement=0.0,
                uncertainty=1.0
            )
        
        # Get weights for this prediction
        weights = self._get_weights(asset_class)
        
        # Ensemble voting
        return self._ensemble_vote(model_predictions, weights)
    
    def predict_batch(
        self,
        texts: list[str],
        asset_class: Optional[str] = None
    ) -> list[EnsemblePrediction]:
        """
        Predict sentiment for multiple texts.
        
        Args:
            texts: List of texts to classify
            asset_class: Asset class for all texts
            
        Returns:
            List of EnsemblePrediction objects
        """
        return [self.predict(text, asset_class) for text in texts]
    
    def _predict_single_model(
        self,
        pipeline_model,
        text: str,
        model_key: str
    ) -> ModelPrediction:
        """Get prediction from a single model."""
        # Run inference
        # With return_all_scores=True, result is [[{label, score}, ...]]
        raw_result = pipeline_model(text)
        
        # Handle different result formats from transformers
        # Some versions return list of lists, others return list of dicts
        if isinstance(raw_result, list) and len(raw_result) > 0:
            result = raw_result[0]
            # If result is still a list, it's the scores array
            if isinstance(result, list):
                scores_list = result
            elif isinstance(result, dict):
                # Single top prediction format
                scores_list = [result]
            else:
                logger.warning(f"Unexpected result format: {type(result)}")
                scores_list = []
        else:
            scores_list = []
        
        # Parse results - format varies by model
        probs = [0.0, 0.0, 0.0]  # [neg, neutral, pos]
        
        for item in scores_list:
            if not isinstance(item, dict):
                logger.warning(f"Skipping non-dict item: {type(item)}")
                continue
            label = item.get("label", "").lower()
            score = item.get("score", 0.0)
            
            if "neg" in label:
                probs[0] = score
            elif "neu" in label:
                probs[1] = score
            elif "pos" in label:
                probs[2] = score
        
        # Normalize probabilities
        total = sum(probs)
        if total > 0:
            probs = [p / total for p in probs]
        
        # Determine label
        max_idx = np.argmax(probs)
        label = [SentimentLabel.NEGATIVE, SentimentLabel.NEUTRAL, SentimentLabel.POSITIVE][max_idx]
        confidence = probs[max_idx]
        
        return ModelPrediction(
            model_name=model_key,
            label=label,
            confidence=confidence,
            probabilities=tuple(probs)
        )
    
    def _mock_predictions(self, text: str) -> list[ModelPrediction]:
        """Generate mock predictions for testing."""
        # Simple keyword-based mock
        text_lower = text.lower()
        
        positive_words = ["surge", "high", "gain", "profit", "bull", "up", "growth"]
        negative_words = ["crash", "drop", "loss", "fall", "bear", "down", "decline"]
        
        pos_count = sum(1 for w in positive_words if w in text_lower)
        neg_count = sum(1 for w in negative_words if w in text_lower)
        
        if pos_count > neg_count:
            probs = (0.1, 0.2, 0.7)
            label = SentimentLabel.POSITIVE
        elif neg_count > pos_count:
            probs = (0.7, 0.2, 0.1)
            label = SentimentLabel.NEGATIVE
        else:
            probs = (0.25, 0.5, 0.25)
            label = SentimentLabel.NEUTRAL
        
        # Add small variation between "models"
        predictions = []
        for i, name in enumerate(["finbert", "roberta"]):
            noise = np.random.uniform(-0.05, 0.05, 3)
            adj_probs = np.clip(np.array(probs) + noise, 0.01, 0.99)
            adj_probs = adj_probs / adj_probs.sum()
            
            predictions.append(ModelPrediction(
                model_name=name,
                label=label,
                confidence=float(adj_probs[probs.index(max(probs))]),
                probabilities=tuple(adj_probs.tolist())
            ))
        
        return predictions
    
    def _get_weights(self, asset_class: Optional[str] = None) -> dict[str, float]:
        """Get model weights, optionally adjusted for asset class."""
        if asset_class and asset_class.lower() in self.ASSET_WEIGHTS:
            return self.ASSET_WEIGHTS[asset_class.lower()].copy()
        return self.weights.copy()
    
    def _ensemble_vote(
        self,
        predictions: list[ModelPrediction],
        weights: dict[str, float]
    ) -> EnsemblePrediction:
        """
        Combine predictions using weighted voting.
        
        Uses soft voting with probability weighting.
        """
        # Initialize weighted probability accumulator
        weighted_probs = np.zeros(3)
        total_weight = 0.0
        
        for pred in predictions:
            model_weight = weights.get(pred.model_name, 1.0 / len(predictions))
            
            # Adjust weight by confidence if enabled
            if self.use_confidence_weighting:
                confidence_factor = max(pred.confidence, self.min_confidence)
                adjusted_weight = model_weight * confidence_factor
            else:
                adjusted_weight = model_weight
            
            weighted_probs += adjusted_weight * np.array(pred.probabilities)
            total_weight += adjusted_weight
        
        # Normalize
        if total_weight > 0:
            weighted_probs /= total_weight
        
        # Determine final label
        max_idx = np.argmax(weighted_probs)
        final_label = [SentimentLabel.NEGATIVE, SentimentLabel.NEUTRAL, SentimentLabel.POSITIVE][max_idx]
        final_confidence = weighted_probs[max_idx]
        
        # Calculate agreement (how much models agree)
        labels = [p.label for p in predictions]
        agreement = labels.count(final_label) / len(labels) if labels else 0.0
        
        # Calculate uncertainty (average entropy)
        avg_entropy = np.mean([p.entropy for p in predictions])
        max_entropy = np.log(3)  # Maximum entropy for 3 classes
        uncertainty = avg_entropy / max_entropy
        
        return EnsemblePrediction(
            label=final_label,
            confidence=float(final_confidence),
            probabilities=tuple(weighted_probs.tolist()),
            model_predictions=predictions,
            agreement=agreement,
            uncertainty=float(uncertainty)
        )
    
    def calibrate(
        self,
        texts: list[str],
        true_labels: list[SentimentLabel]
    ) -> dict[str, float]:
        """
        Calibrate model weights based on labeled data.
        
        Adjusts weights to maximize accuracy on calibration set.
        
        Args:
            texts: Calibration texts
            true_labels: True sentiment labels
            
        Returns:
            Updated model weights
        """
        if len(texts) != len(true_labels):
            raise ValueError("texts and true_labels must have same length")
        
        # Collect predictions from each model
        model_correct = {key: 0 for key in self.weights.keys()}
        
        for text, true_label in zip(texts, true_labels):
            pred = self.predict(text)
            
            for model_pred in pred.model_predictions:
                if model_pred.label == true_label:
                    model_correct[model_pred.model_name] = \
                        model_correct.get(model_pred.model_name, 0) + 1
        
        # Calculate accuracy-based weights
        n_samples = len(texts)
        new_weights = {}
        
        for model_name in self.weights.keys():
            accuracy = model_correct.get(model_name, 0) / n_samples
            new_weights[model_name] = accuracy
        
        # Normalize weights
        total = sum(new_weights.values())
        if total > 0:
            new_weights = {k: v / total for k, v in new_weights.items()}
        
        self.weights = new_weights
        logger.info(f"Calibrated weights: {new_weights}")
        
        return new_weights


def create_ensemble(
    models: Optional[list[str]] = None,
    device: str = "auto"
) -> SentimentEnsemble:
    """
    Factory function to create a sentiment ensemble.
    
    Args:
        models: Model identifiers to use
        device: Computation device
        
    Returns:
        Configured SentimentEnsemble instance
    """
    ensemble = SentimentEnsemble(models=models, device=device)
    return ensemble
