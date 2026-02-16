"""
Market regime classifier.

Phase 1: Rule-based regime detection for development.
Phase 2: ML-based (Random Forest / XGBoost) trained on historical data.
Phase 3: HMM for sequential state modeling (future).
"""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import logging
import pickle
from pathlib import Path
from typing import Optional, Any, Dict

import numpy as np
import pandas as pd

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
    
    # Optional external indicators
    vix_level: Optional[float] = None
    ciss_level: Optional[float] = None  # ECB CISS stress index
    
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
            "ciss_level": self.ciss_level,
        }


class RegimeClassifier:
    """
    Market regime classifier based on sentiment features.
    
    Phase 1 (Current): Rule-based thresholds
    Phase 2: ML-based (Random Forest / XGBoost)
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


class MLRegimeClassifier(RegimeClassifier):
    """
    ML-based regime classifier using trained Random Forest or XGBoost.
    
    Loads pre-trained model from disk and provides inference.
    Falls back to rule-based classification if model not available.
    """
    
    # Default model path (relative to project root)
    DEFAULT_MODEL_PATH = "models/regime_classifier_best.pkl"
    
    def __init__(
        self, 
        model_path: Optional[str] = None,
        model_type: str = "best",
    ):
        """
        Initialize ML classifier.
        
        Args:
            model_path: Path to trained model pickle file
            model_type: One of 'best', 'rf', 'xgb' to load specific model
        """
        super().__init__(model_version=f"ml-{model_type}-v1")
        
        # Determine model path
        if model_path is None:
            project_root = Path(__file__).parent.parent.parent.parent
            if model_type == "rf":
                model_path = str(project_root / "models" / "regime_classifier_rf.pkl")
            elif model_type == "xgb":
                model_path = str(project_root / "models" / "regime_classifier_xgb.pkl")
            else:
                model_path = str(project_root / self.DEFAULT_MODEL_PATH)
        
        self.model_path = model_path
        self._model = None
        self._scaler = None
        self._feature_names: list = []
        self._label_map: Dict[str, int] = {}
        self._reverse_label_map: Dict[int, str] = {}
        self._model_type: str = ""
        
        self._load_model()
    
    def _load_model(self) -> None:
        """Load trained ML model from pickle file."""
        try:
            model_file = Path(self.model_path)
            if not model_file.exists():
                logger.warning(f"Model file not found: {self.model_path}")
                logger.warning("Using rule-based fallback")
                return
            
            with open(model_file, 'rb') as f:
                checkpoint = pickle.load(f)
            
            self._model = checkpoint['model']
            self._scaler = checkpoint['scaler']
            self._feature_names = checkpoint['feature_names']
            self._label_map = checkpoint.get('label_map', {'risk_on': 0, 'transition': 1, 'risk_off': 2})
            self._reverse_label_map = {v: k for k, v in self._label_map.items()}
            self._model_type = checkpoint.get('model_type', 'unknown')
            
            metrics = checkpoint.get('metrics', {})
            f1_value = metrics.get('f1_weighted')
            if isinstance(f1_value, (int, float)):
                f1_display = f"{f1_value:.4f}"
            else:
                f1_display = "N/A"
            logger.info("ML model loaded: %s (F1: %s)", self._model_type, f1_display)
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            self._model = None
    
    def _prepare_features(self, features: SentimentFeatures) -> Optional[pd.DataFrame]:
        """
        Prepare feature vector for ML model.
        
        Maps SentimentFeatures to the feature set used during training.
        Note: CISS features are the most important predictors. If ciss_level
        is not provided, the model will have reduced accuracy.
        """
        # Build feature dict from SentimentFeatures
        feature_dict = {
            'sentiment': features.cross_asset_mean,
            'sentiment_change': features.sentiment_momentum,
            'sentiment_momentum_5d': features.sentiment_momentum,
            'sentiment_momentum_20d': features.sentiment_momentum,
            'sentiment_ma5': features.cross_asset_mean,
            'sentiment_ma20': features.cross_asset_mean,
            'sentiment_acceleration': features.sentiment_acceleration,
            'sentiment_dispersion': features.cross_asset_std,
            'sentiment_spread': features.cross_asset_mean,  # Approximation
            'cross_asset_divergence': features.max_divergence,
        }
        
        # Add CISS features if available (most important for predictions)
        if features.ciss_level is not None:
            feature_dict.update({
                'ciss_lag1': features.ciss_level,
                'ciss_change': 0.0,  # Would need historical data
                'ciss_change_5d': 0.0,
                'ciss_ma5': features.ciss_level,
                'ciss_ma20': features.ciss_level,
                'ciss_above_ma20': 0,
                'ciss_std_20d': 0.05,  # Default std
                'ciss_trend': 0,
            })
        
        # Add VIX features if available
        if features.vix_level is not None:
            vix = features.vix_level
            feature_dict.update({
                'vix': vix,
                'vix_change': 0.0,  # Would need historical data
                'vix_change_pct': 0.0,
                'vix_ma5': vix,
                'vix_ma20': vix,
                'vix_above_ma20': 0,
                'vix_spike': 1 if vix > 30 else 0,
                'vix_range': vix * 0.05,  # Approximate daily range
            })
            
            # Interaction features
            if features.ciss_level is not None:
                feature_dict['ciss_vix_ratio'] = features.ciss_level / (vix / 100 + 0.01)
            feature_dict['sentiment_vix_interaction'] = features.cross_asset_mean * (1 / (vix + 1))
        
        # Create DataFrame with correct feature order
        try:
            feature_vector = {}
            for name in self._feature_names:
                if name in feature_dict:
                    feature_vector[name] = feature_dict[name]
                else:
                    # Use 0 for missing features (not ideal but prevents errors)
                    feature_vector[name] = 0.0
                    logger.debug(f"Missing feature: {name}, using 0.0")
            
            df = pd.DataFrame([feature_vector])
            return df
            
        except Exception as e:
            logger.error(f"Error preparing features: {e}")
            return None
    
    def classify(self, features: SentimentFeatures) -> RegimeClassification:
        """
        Classify market regime using trained ML model.
        
        Falls back to rule-based if model not loaded.
        """
        if self._model is None:
            logger.warning("ML model not loaded, using rule-based classification")
            return super().classify(features)
        
        try:
            # Prepare features
            feature_df = self._prepare_features(features)
            if feature_df is None:
                return super().classify(features)
            
            # Scale features
            feature_scaled = self._scaler.transform(feature_df)
            
            # Predict
            if hasattr(self._model, 'predict_proba'):
                probas = self._model.predict_proba(feature_scaled)[0]
                predicted_class = np.argmax(probas)
                
                # Map probabilities to states
                # Ensure correct ordering based on label_map
                prob_risk_on = probas[self._label_map.get('risk_on', 0)]
                prob_transition = probas[self._label_map.get('transition', 1)]
                prob_risk_off = probas[self._label_map.get('risk_off', 2)]
            else:
                # Model doesn't support predict_proba
                predicted_class = self._model.predict(feature_scaled)[0]
                prob_risk_on = 1.0 if predicted_class == self._label_map['risk_on'] else 0.0
                prob_transition = 1.0 if predicted_class == self._label_map['transition'] else 0.0
                prob_risk_off = 1.0 if predicted_class == self._label_map['risk_off'] else 0.0
            
            # Map prediction to state
            state_str = self._reverse_label_map.get(predicted_class, 'transition')
            state = RegimeState(state_str)
            
            # Confidence is the probability of the predicted class
            confidence = max(prob_risk_on, prob_transition, prob_risk_off)
            
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
            
        except Exception as e:
            logger.error(f"ML classification failed: {e}")
            return super().classify(features)
    
    def classify_batch(
        self, 
        features_df: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Classify multiple samples at once.
        
        Args:
            features_df: DataFrame with feature columns matching training features
            
        Returns:
            DataFrame with predictions and probabilities
        """
        if self._model is None:
            raise ValueError("Model not loaded")
        
        # Ensure correct feature order
        features_ordered = features_df[self._feature_names]
        features_scaled = self._scaler.transform(features_ordered)
        
        # Predict
        predictions = self._model.predict(features_scaled)
        
        if hasattr(self._model, 'predict_proba'):
            probas = self._model.predict_proba(features_scaled)
            result = pd.DataFrame({
                'predicted_regime': [self._reverse_label_map[p] for p in predictions],
                'prob_risk_on': probas[:, self._label_map['risk_on']],
                'prob_transition': probas[:, self._label_map['transition']],
                'prob_risk_off': probas[:, self._label_map['risk_off']],
            }, index=features_df.index)
        else:
            result = pd.DataFrame({
                'predicted_regime': [self._reverse_label_map[p] for p in predictions],
            }, index=features_df.index)
        
        return result
    
    @property
    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self._model is not None
    
    @property
    def feature_importance(self) -> Optional[Dict[str, float]]:
        """Get feature importances from the model."""
        if self._model is None:
            return None
        
        if hasattr(self._model, 'feature_importances_'):
            return dict(zip(self._feature_names, self._model.feature_importances_))
        return None


class HMMRegimeClassifier(RegimeClassifier):
    """
    Hidden Markov Model-based regime classifier.
    
    Placeholder for Phase 3 implementation for sequential state modeling.
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
        # TODO: Implement HMM training on MANEFRAME
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
