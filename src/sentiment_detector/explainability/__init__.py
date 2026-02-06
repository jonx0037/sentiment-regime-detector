"""SHAP-based explainability for regime classifier."""

from .explainer import RegimeExplainer, ExplanationResult
from .cache import ExplainabilityCache
from .events import CrisisEvent, CRISIS_EVENTS, get_event, list_events
from . import viz

__all__ = [
    'RegimeExplainer',
    'ExplanationResult',
    'ExplainabilityCache',
    'CrisisEvent',
    'CRISIS_EVENTS',
    'get_event',
    'list_events',
    'viz',
]
