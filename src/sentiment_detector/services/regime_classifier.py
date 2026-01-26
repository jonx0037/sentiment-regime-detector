"""
Market regime classifier.

Phase 1: Rule-based regime detection for development.
Phase 2: HMM + Gradient Boosting trained on MANEFRAME.
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import logging
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)


class RegimeState(str, Enum):
    """Market regime states."""
    RISK_ON = "risk_on"
    RISK_OFF = "risk_off"
    TRANSITION = "transition"


@dataclass
class RegimeClassification:
    """Regime classification result."""
    state: RegimeState
    confidence: float
    prob_risk_on: float
    prob_risk_off: float
    prob_transition: float
    timestamp: datetime
    features_used: dict
    model_version: str


@dataclass
class SentimentFeatures:
    """Aggregated sentiment features for regime classification."""
    # Cross-asset sentiment
    equity_sentiment: float
    crypto_sentiment: float
    forex_sentiment: float  # USD strength proxy
    commodity_sentiment: float
    
    # Aggregate metrics
    cross_asset_mean: float
    cross_asset_std: float
    
    # Momentum (7-day rolling)
    sentiment_momentum: float  # Rate of change
    sentiment_acceleration: float
    
    # Divergence
    max_divergence: float  # Max difference between asset classes
    
    # Optional external
    vix_level: Optional[float] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        return {
            "equity_sentiment": self.equity_sentiment,
            "crypto_sentiment": self.crypto_sentiment,
            "forex_sentiment": self.forex_sentiment,
            "commodity_sentiment": self.commodity_sentiment,
            "cross_asset_mean": self.cross_asset_mean,
            "cross_asset_std": self.cross_asset_std,
            "sentiment_momentum": self.sentiment_momentum,
            "sentiment_acceleration": self.sentiment_acceleration,
            "max_divergence": self.max_divergence,
            "vix_level": self.vix_level,
        }


class RegimeClassifier:
    """
    Market regime classifier based on sentiment features.
    
    Phase 1 (Current): Rule-based thresholds
    Phase 2 (MANEFRAME): Hidden Markov Model + Gradient Boosting
    """
    
    # Thresholds for rule-based classification
    RISK_ON_THRESHOLD = 0.15
    RISK_OFF_THRESHOLD = -0.15
    VOLATILITY_THRESHOLD = 0.25
    DIVERGENCE_THRESHOLD = 0.4
    
    def __init__(self, model_version: str = "rule-based-v1"):
        """
        Initialize regime classifier.
        
        Args:
            model_version: Version string for tracking
        """
        self.model_version = model_version
        logger.info(f"RegimeClassifier initialized: {model_version}")
    
    def classify(self, features: SentimentFeatures) -> RegimeClassification:
        """
        Classify current market regime based on sentiment features.
        
        Args:
            features: Aggregated sentiment features
            
        Returns:
            RegimeClassification with state, confidence, and probabilities
        """
        # Calculate base probabilities from rules
        prob_risk_on, prob_risk_off, prob_transition = self._calculate_probabilities(features)
        
        # Normalize to sum to 1
        total = prob_risk_on + prob_risk_off + prob_transition
        prob_risk_on /= total
        prob_risk_off /= total
        prob_transition /= total
        
        # Determine state from highest probability
        probs = {
            RegimeState.RISK_ON: prob_risk_on,
            RegimeState.RISK_OFF: prob_risk_off,
            RegimeState.TRANSITION: prob_transition,
        }
        state = max(probs, key=probs.get)
        confidence = probs[state]
        
        return RegimeClassification(
            state=state,
            confidence=confidence,
            prob_risk_on=prob_risk_on,
            prob_risk_off=prob_risk_off,
            prob_transition=prob_transition,
            timestamp=datetime.utcnow(),
            features_used=features.to_dict(),
            model_version=self.model_version,
        )
    
    def _calculate_probabilities(self, features: SentimentFeatures) -> tuple[float, float, float]:
        """
        Calculate raw probabilities for each regime state.
        
        Uses a rule-based approach with soft thresholds.
        """
        mean = features.cross_asset_mean
        std = features.cross_asset_std
        momentum = features.sentiment_momentum
        divergence = features.max_divergence
        
        # Risk-On indicators
        risk_on_score = 0.0
        if mean > self.RISK_ON_THRESHOLD:
            risk_on_score += 0.4 * min(mean / 0.5, 1.0)  # Cap contribution
        if momentum > 0:
            risk_on_score += 0.2 * min(momentum / 0.3, 1.0)
        if std < self.VOLATILITY_THRESHOLD:
            risk_on_score += 0.2 * (1 - std / self.VOLATILITY_THRESHOLD)
        if divergence < self.DIVERGENCE_THRESHOLD:
            risk_on_score += 0.2 * (1 - divergence / self.DIVERGENCE_THRESHOLD)
        
        # Risk-Off indicators
        risk_off_score = 0.0
        if mean < self.RISK_OFF_THRESHOLD:
            risk_off_score += 0.4 * min(abs(mean) / 0.5, 1.0)
        if momentum < 0:
            risk_off_score += 0.2 * min(abs(momentum) / 0.3, 1.0)
        if std > self.VOLATILITY_THRESHOLD:
            risk_off_score += 0.2 * min(std / 0.5, 1.0)
        
        # VIX adjustment if available
        if features.vix_level is not None:
            if features.vix_level > 30:
                risk_off_score += 0.15
            elif features.vix_level < 15:
                risk_on_score += 0.1
        
        # Transition indicators
        transition_score = 0.0
        if abs(mean) < self.RISK_ON_THRESHOLD:
            transition_score += 0.3
        if divergence > self.DIVERGENCE_THRESHOLD:
            transition_score += 0.3
        if abs(momentum) < 0.05:
            transition_score += 0.2
        
        # Ensure minimum probabilities
        risk_on_score = max(risk_on_score, 0.1)
        risk_off_score = max(risk_off_score, 0.1)
        transition_score = max(transition_score, 0.1)
        
        return risk_on_score, risk_off_score, transition_score
    
    def detect_transition(
        self,
        current: RegimeClassification,
        previous: RegimeClassification,
    ) -> Optional[dict]:
        """
        Detect if a regime transition has occurred.
        
        Args:
            current: Current regime classification
            previous: Previous regime classification
            
        Returns:
            Transition info dict if transition detected, None otherwise
        """
        if current.state != previous.state:
            return {
                "from_regime": previous.state.value,
                "to_regime": current.state.value,
                "transition_start": previous.timestamp,
                "confidence": current.confidence,
                "trigger_features": current.features_used,
            }
        return None


class HMMRegimeClassifier(RegimeClassifier):
    """
    Hidden Markov Model-based regime classifier.
    
    Placeholder for Phase 2 implementation after MANEFRAME training.
    """
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize HMM classifier.
        
        Args:
            model_path: Path to trained HMM model checkpoint
        """
        super().__init__(model_version="hmm-v1")
        self.model_path = model_path
        self._model = None
        
        if model_path:
            self._load_model()
    
    def _load_model(self) -> None:
        """Load trained HMM model from checkpoint."""
        # TODO: Implement after MANEFRAME training
        logger.warning("HMM model loading not yet implemented - using rule-based fallback")
    
    def classify(self, features: SentimentFeatures) -> RegimeClassification:
        """
        Classify using HMM model.
        
        Falls back to rule-based if model not loaded.
        """
        if self._model is None:
            logger.warning("HMM model not loaded, using rule-based classification")
            return super().classify(features)
        
        # TODO: Implement HMM inference
        raise NotImplementedError("HMM inference not yet implemented")
