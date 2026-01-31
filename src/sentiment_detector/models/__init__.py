"""SQLAlchemy ORM models and ML models."""

from sentiment_detector.models.base import Base, TimestampMixin
from sentiment_detector.models.text_record import RawText
from sentiment_detector.models.sentiment import SentimentScore, SentimentIndex
from sentiment_detector.models.regime import RegimeState, RegimeTransition

# ML Models
from sentiment_detector.models.garch_midas import (
    GARCHMIDASModel,
    GARCHMIDASResult,
    MIDASWeights,
)
from sentiment_detector.models.jump_model import (
    StatisticalJumpModel,
    JumpModelConfig,
    JumpModelResult,
    RegimeCentroid,
    create_feature_matrix,
)

__all__ = [
    # ORM Models
    "Base",
    "TimestampMixin",
    "RawText",
    "SentimentScore",
    "SentimentIndex",
    "RegimeState",
    "RegimeTransition",
    # ML Models - GARCH-MIDAS
    "GARCHMIDASModel",
    "GARCHMIDASResult",
    "MIDASWeights",
    # ML Models - Jump Model
    "StatisticalJumpModel",
    "JumpModelConfig",
    "JumpModelResult",
    "RegimeCentroid",
    "create_feature_matrix",
]
