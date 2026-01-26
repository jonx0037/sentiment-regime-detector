"""
Sentiment analysis engine using transformer models.

Phase 1: Uses DistilBERT for CPU-friendly local inference.
Phase 2: Will swap to fine-tuned FinBERT + RoBERTa ensemble from MANEFRAME.
"""

from dataclasses import dataclass
from enum import Enum
import logging
from typing import Optional

import torch
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification

logger = logging.getLogger(__name__)


class SentimentLabel(str, Enum):
    """Sentiment classification labels."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


@dataclass
class SentimentScore:
    """Sentiment analysis result for a single text."""
    label: SentimentLabel
    positive: float
    negative: float
    neutral: float
    compound: float  # Aggregated score [-1, 1]
    confidence: float
    model_name: str


class SentimentEngine:
    """
    Multi-model sentiment analysis engine.
    
    Supports:
    - DistilBERT (default, CPU-friendly for development)
    - FinBERT (finance-specific, requires fine-tuning)
    - RoBERTa (general purpose, strong baseline)
    """
    
    # Model configurations
    MODEL_CONFIGS = {
        "distilbert": {
            "name": "distilbert-base-uncased-finetuned-sst-2-english",
            "max_length": 512,
            "labels": {"POSITIVE": "positive", "NEGATIVE": "negative"},
        },
        "finbert": {
            "name": "ProsusAI/finbert",
            "max_length": 512,
            "labels": {"positive": "positive", "negative": "negative", "neutral": "neutral"},
        },
        "roberta": {
            "name": "cardiffnlp/twitter-roberta-base-sentiment-latest",
            "max_length": 512,
            "labels": {"positive": "positive", "negative": "negative", "neutral": "neutral"},
        },
    }
    
    def __init__(
        self,
        model_type: str = "distilbert",
        device: Optional[str] = None,
        batch_size: int = 32,
    ):
        """
        Initialize sentiment engine.
        
        Args:
            model_type: One of 'distilbert', 'finbert', 'roberta'
            device: 'cpu', 'cuda', or 'mps' (Apple Silicon). Auto-detects if None.
            batch_size: Batch size for inference
        """
        self.model_type = model_type
        self.batch_size = batch_size
        
        # Auto-detect device
        if device is None:
            if torch.cuda.is_available():
                self.device = "cuda"
            elif torch.backends.mps.is_available():
                self.device = "mps"
            else:
                self.device = "cpu"
        else:
            self.device = device
            
        self.config = self.MODEL_CONFIGS.get(model_type)
        if not self.config:
            raise ValueError(f"Unknown model type: {model_type}. Choose from {list(self.MODEL_CONFIGS.keys())}")
        
        self._pipeline = None
        self._loaded = False
        
        logger.info(f"SentimentEngine initialized: model={model_type}, device={self.device}")
    
    def load(self) -> None:
        """Load the model into memory."""
        if self._loaded:
            return
            
        logger.info(f"Loading model: {self.config['name']}")
        
        # Use -1 for CPU, otherwise use device index
        device_num = -1 if self.device == "cpu" else 0
        
        self._pipeline = pipeline(
            "sentiment-analysis",
            model=self.config["name"],
            tokenizer=self.config["name"],
            device=device_num,
            truncation=True,
            max_length=self.config["max_length"],
        )
        
        self._loaded = True
        logger.info(f"Model loaded successfully on {self.device}")
    
    def analyze(self, text: str) -> SentimentScore:
        """
        Analyze sentiment of a single text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            SentimentScore with label, probabilities, and compound score
        """
        if not self._loaded:
            self.load()
        
        result = self._pipeline(text)[0]
        return self._convert_result(result)
    
    def analyze_batch(self, texts: list[str]) -> list[SentimentScore]:
        """
        Analyze sentiment of multiple texts efficiently.
        
        Args:
            texts: List of input texts
            
        Returns:
            List of SentimentScore objects
        """
        if not self._loaded:
            self.load()
        
        if not texts:
            return []
        
        results = self._pipeline(
            texts,
            batch_size=self.batch_size,
            truncation=True,
        )
        
        return [self._convert_result(r) for r in results]
    
    def _convert_result(self, result: dict) -> SentimentScore:
        """Convert pipeline result to SentimentScore."""
        raw_label = result["label"]
        score = result["score"]
        
        # Map model-specific labels to standard labels
        label_map = self.config["labels"]
        label = label_map.get(raw_label, raw_label).lower()
        
        # Calculate probabilities (simplified for binary models)
        if self.model_type == "distilbert":
            # DistilBERT is binary (positive/negative)
            if label == "positive":
                positive = score
                negative = 1 - score
                neutral = 0.0
            else:
                positive = 1 - score
                negative = score
                neutral = 0.0
        else:
            # For 3-class models, we get the winning class score
            # Full probabilities require additional inference
            positive = score if label == "positive" else 0.0
            negative = score if label == "negative" else 0.0
            neutral = score if label == "neutral" else 0.0
        
        # Compound score: maps to [-1, 1]
        compound = positive - negative
        
        return SentimentScore(
            label=SentimentLabel(label) if label in [e.value for e in SentimentLabel] else SentimentLabel.NEUTRAL,
            positive=positive,
            negative=negative,
            neutral=neutral,
            compound=compound,
            confidence=score,
            model_name=self.model_type,
        )
    
    def __repr__(self) -> str:
        return f"SentimentEngine(model={self.model_type}, device={self.device}, loaded={self._loaded})"


class EnsembleSentimentEngine:
    """
    Weighted ensemble of multiple sentiment models.
    
    Combines predictions from FinBERT, RoBERTa, and DistilBERT
    for more robust sentiment analysis.
    """
    
    DEFAULT_WEIGHTS = {
        "finbert": 0.5,   # Primary: finance-specific
        "roberta": 0.3,   # Secondary: strong general model
        "distilbert": 0.2, # Fallback: fast and reliable
    }
    
    def __init__(
        self,
        weights: Optional[dict[str, float]] = None,
        device: Optional[str] = None,
    ):
        """
        Initialize ensemble engine.
        
        Args:
            weights: Dict mapping model names to weights. Must sum to 1.0.
            device: Device for all models
        """
        self.weights = weights or self.DEFAULT_WEIGHTS
        
        # Validate weights sum to 1
        weight_sum = sum(self.weights.values())
        if abs(weight_sum - 1.0) > 0.01:
            raise ValueError(f"Weights must sum to 1.0, got {weight_sum}")
        
        # Initialize individual engines
        self.engines = {
            name: SentimentEngine(model_type=name, device=device)
            for name in self.weights.keys()
        }
    
    def load(self) -> None:
        """Load all models into memory."""
        for engine in self.engines.values():
            engine.load()
    
    def analyze(self, text: str) -> SentimentScore:
        """
        Analyze text using weighted ensemble.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Weighted average SentimentScore
        """
        scores = {}
        for name, engine in self.engines.items():
            scores[name] = engine.analyze(text)
        
        return self._aggregate_scores(scores)
    
    def _aggregate_scores(self, scores: dict[str, SentimentScore]) -> SentimentScore:
        """Compute weighted average of scores."""
        weighted_positive = sum(
            scores[name].positive * self.weights[name]
            for name in scores
        )
        weighted_negative = sum(
            scores[name].negative * self.weights[name]
            for name in scores
        )
        weighted_neutral = sum(
            scores[name].neutral * self.weights[name]
            for name in scores
        )
        weighted_compound = sum(
            scores[name].compound * self.weights[name]
            for name in scores
        )
        weighted_confidence = sum(
            scores[name].confidence * self.weights[name]
            for name in scores
        )
        
        # Determine label from compound score
        if weighted_compound > 0.1:
            label = SentimentLabel.POSITIVE
        elif weighted_compound < -0.1:
            label = SentimentLabel.NEGATIVE
        else:
            label = SentimentLabel.NEUTRAL
        
        return SentimentScore(
            label=label,
            positive=weighted_positive,
            negative=weighted_negative,
            neutral=weighted_neutral,
            compound=weighted_compound,
            confidence=weighted_confidence,
            model_name="ensemble",
        )
