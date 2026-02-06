# src/sentiment_detector/explainability/explainer.py
import shap
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class ExplanationResult:
    """Result from SHAP explanation."""
    feature_names: List[str]
    feature_values: Dict[str, float]
    shap_values: np.ndarray
    base_value: float
    prediction: float
    confidence: float
    predicted_regime: str
    timestamp: datetime
    model_version: str

    def to_dict(self) -> dict:
        """Serialize to JSON (no pickle for security)."""
        return {
            'feature_names': self.feature_names,
            'feature_values': self.feature_values,
            'shap_values': self.shap_values.tolist(),
            'base_value': float(self.base_value),
            'prediction': float(self.prediction),
            'confidence': float(self.confidence),
            'predicted_regime': self.predicted_regime,
            'timestamp': self.timestamp.isoformat(),
            'model_version': self.model_version,
        }

class RegimeExplainer:
    """SHAP-based explainability for regime classifier."""

    def __init__(self, model_path: str = "models/regime_classifier_best.pkl", cache=None):
        """Initialize explainer.

        Args:
            model_path: Path to trained model pickle file
            cache: Optional ExplainabilityCache for caching (async operations)
        """
        self.model_path = Path(model_path)
        self._model = None
        self._scaler = None
        self._feature_names = None
        self._explainer = None
        self.model_version = None
        self.cache = cache

    def _load_model(self):
        """Load model from trusted pickle checkpoint."""
        import pickle

        with open(self.model_path, 'rb') as f:
            checkpoint = pickle.load(f)

        self._model = checkpoint['model']
        self._scaler = checkpoint['scaler']
        self._feature_names = checkpoint['feature_names']
        self.model_version = checkpoint.get('model_version', 'unknown')

        # Initialize SHAP
        self._explainer = shap.TreeExplainer(self._model)
        logger.info(f"Loaded model with {len(self._feature_names)} features")

    def explain_prediction(self, features: Dict[str, float]) -> ExplanationResult:
        """Explain prediction using SHAP TreeExplainer."""
        if self._model is None:
            self._load_model()

        # Prepare features in correct order
        feature_vector = pd.DataFrame(
            [[features[name] for name in self._feature_names]],
            columns=self._feature_names,
        )

        # Scale
        feature_scaled = self._scaler.transform(feature_vector)

        # Prediction first (needed for SHAP value extraction)
        probas = self._model.predict_proba(feature_scaled)[0]
        prediction = np.argmax(probas)
        confidence = probas[prediction]

        # SHAP values
        shap_values = self._explainer.shap_values(feature_scaled)

        # Handle multi-class - extract SHAP values for predicted class
        if isinstance(shap_values, list):
            # Some models return list of arrays (one per class)
            shap_values = shap_values[prediction][0]
        elif len(shap_values.shape) == 3:
            # Shape: (n_samples, n_features, n_classes)
            shap_values = shap_values[0, :, prediction]
        elif len(shap_values.shape) == 2:
            # Shape: (n_features, n_classes) - get predicted class column
            shap_values = shap_values[:, prediction]
        else:
            # Binary or already extracted
            shap_values = shap_values[0] if len(shap_values.shape) > 1 else shap_values

        # Map to regime
        label_map = {0: 'risk_on', 1: 'transition', 2: 'risk_off'}
        predicted_regime = label_map[prediction]

        # Base value
        base_value = self._explainer.expected_value
        if isinstance(base_value, np.ndarray):
            base_value = base_value[prediction]

        # For multi-class, prediction should be the raw model output (probability)
        # for SHAP additivity to work correctly
        raw_prediction = probas[prediction]

        return ExplanationResult(
            feature_names=self._feature_names,
            feature_values=features,
            shap_values=shap_values,
            base_value=float(base_value),
            prediction=float(raw_prediction),  # Use probability, not class index
            confidence=float(confidence),
            predicted_regime=predicted_regime,
            timestamp=datetime.utcnow(),
            model_version=self.model_version,
        )

    async def explain_prediction_async(self, features: Dict[str, float]) -> ExplanationResult:
        """Async version of explain_prediction with caching support.

        Args:
            features: Dictionary of feature name -> value (all 28 required)

        Returns:
            ExplanationResult with SHAP values and prediction

        Note:
            Requires cache to be configured in __init__. Falls back to computation
            if cache is not available or encounters errors.
        """
        if self._model is None:
            self._load_model()

        # Check cache if available
        if self.cache:
            from .cache import ExplainabilityCache
            cache_key = ExplainabilityCache.make_cache_key(self.model_version, features)

            try:
                cached = await self.cache.get(cache_key)
                if cached:
                    # Deserialize from JSON
                    cached['shap_values'] = np.array(cached['shap_values'])
                    cached['timestamp'] = datetime.fromisoformat(cached['timestamp'])
                    return ExplanationResult(**cached)
            except Exception as e:
                logger.warning(f"Cache get error: {e}, computing fresh")

        # Compute fresh explanation (same logic as sync version)
        feature_vector = pd.DataFrame(
            [[features[name] for name in self._feature_names]],
            columns=self._feature_names,
        )

        feature_scaled = self._scaler.transform(feature_vector)

        # Prediction first
        probas = self._model.predict_proba(feature_scaled)[0]
        prediction = np.argmax(probas)
        confidence = probas[prediction]

        # SHAP values
        shap_values = self._explainer.shap_values(feature_scaled)

        # Handle multi-class
        if isinstance(shap_values, list):
            shap_values = shap_values[prediction][0]
        elif len(shap_values.shape) == 3:
            shap_values = shap_values[0, :, prediction]
        elif len(shap_values.shape) == 2:
            shap_values = shap_values[:, prediction]
        else:
            shap_values = shap_values[0] if len(shap_values.shape) > 1 else shap_values

        # Map to regime
        label_map = {0: 'risk_on', 1: 'transition', 2: 'risk_off'}
        predicted_regime = label_map[prediction]

        # Base value
        base_value = self._explainer.expected_value
        if isinstance(base_value, np.ndarray):
            base_value = base_value[prediction]

        raw_prediction = probas[prediction]

        result = ExplanationResult(
            feature_names=self._feature_names,
            feature_values=features,
            shap_values=shap_values,
            base_value=float(base_value),
            prediction=float(raw_prediction),
            confidence=float(confidence),
            predicted_regime=predicted_regime,
            timestamp=datetime.utcnow(),
            model_version=self.model_version,
        )

        # Cache result if cache available
        if self.cache:
            try:
                await self.cache.set(cache_key, result.to_dict())
            except Exception as e:
                logger.warning(f"Cache set error: {e}")

        return result

    def global_importance(self, features_df: pd.DataFrame) -> Dict[str, float]:
        """Compute mean(|SHAP|) across samples.

        Args:
            features_df: DataFrame with samples (rows) and features (columns)
                        Must have same columns as training features

        Returns:
            Dictionary mapping feature names to mean absolute SHAP values
        """
        if self._model is None:
            self._load_model()

        # Ensure features are in correct order
        features_df = features_df[self._feature_names]

        # Scale features
        features_scaled = self._scaler.transform(features_df)

        # Get SHAP values
        shap_values = self._explainer.shap_values(features_scaled)

        # Handle multi-class: average across classes and samples
        if isinstance(shap_values, list):
            # List of arrays (one per class)
            shap_values = np.stack(shap_values)  # Shape: (n_classes, n_samples, n_features)
            shap_values = np.mean(np.abs(shap_values), axis=(0, 1))  # Average over classes and samples
        elif len(shap_values.shape) == 3:
            # Shape: (n_samples, n_features, n_classes)
            shap_values = np.mean(np.abs(shap_values), axis=(0, 2))  # Average over samples and classes
        elif len(shap_values.shape) == 2:
            # Shape: (n_samples, n_features) - binary or single class
            shap_values = np.mean(np.abs(shap_values), axis=0)  # Average over samples
        else:
            raise ValueError(f"Unexpected SHAP values shape: {shap_values.shape}")

        return dict(zip(self._feature_names, shap_values))

    def feature_interactions(self, features_df: pd.DataFrame, top_k: int = 10) -> dict:
        """Compute SHAP interaction values to identify synergistic feature effects.

        Args:
            features_df: DataFrame with samples (rows) and features (columns)
            top_k: Number of top interaction pairs to return

        Returns:
            Dictionary with:
                - top_interactions: List of (feature1, feature2, interaction_strength) tuples
                - interaction_matrix: Full interaction matrix as nested list
                - feature_names: List of feature names for matrix indexing
        """
        if self._model is None:
            self._load_model()

        # Ensure features are in correct order
        features_df = features_df[self._feature_names]

        # Scale features
        features_scaled = self._scaler.transform(features_df)

        # Get SHAP interaction values
        interaction_values = self._explainer.shap_interaction_values(features_scaled)

        # Handle multi-class: average across classes and samples
        if isinstance(interaction_values, list):
            # List of arrays (one per class)
            interaction_values = np.stack(interaction_values)  # Shape: (n_classes, n_samples, n_features, n_features)
            avg_interactions = np.mean(np.abs(interaction_values), axis=(0, 1))  # Average over classes and samples
        elif len(interaction_values.shape) == 4:
            # Shape: (n_samples, n_features, n_features, n_classes) or similar
            # Find the axes that correspond to samples and classes, average over them
            avg_interactions = np.mean(np.abs(interaction_values), axis=(0, 3))
        elif len(interaction_values.shape) == 3:
            # Shape: (n_samples, n_features, n_features)
            avg_interactions = np.mean(np.abs(interaction_values), axis=0)
        else:
            raise ValueError(f"Unexpected interaction values shape: {interaction_values.shape}")

        # Extract top-k pairs (exclude diagonal - self-interactions)
        pairs = []
        n = len(self._feature_names)
        for i in range(n):
            for j in range(i + 1, n):
                pairs.append((
                    self._feature_names[i],
                    self._feature_names[j],
                    float(avg_interactions[i, j])
                ))

        pairs.sort(key=lambda x: abs(x[2]), reverse=True)

        return {
            'top_interactions': pairs[:top_k],
            'interaction_matrix': avg_interactions.tolist(),
            'feature_names': self._feature_names,
        }
