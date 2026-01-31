"""
Feature engineering module for sentiment regime detection.

This module contains advanced feature extraction including:
- Sentiment connectedness (Cao et al., 2025) - entropy-based network metrics
- Transfer entropy divergence (Caferra, 2022) - Rényi transfer entropy
- Granger causality analysis - nonlinear methods via nitime

These features are critical for:
- H2 (Divergence Signal Hypothesis) validation
- H3 (Network Effect Hypothesis) validation
"""

from .granger_causality import (
    GrangerCausalityAnalyzer,
    GrangerResult,
    CausalityNetwork,
    granger_causality_test,
)
from .transfer_entropy import (
    TransferEntropyAnalyzer,
    TransferEntropyResult,
    InformationFlowNetwork,
    transfer_entropy,
)
from .connectedness import (
    ConnectednessAnalyzer,
    ConnectednessResult,
    DynamicConnectedness,
    calculate_centrality,
    identify_key_transmitters,
)

__all__ = [
    # Granger Causality
    "GrangerCausalityAnalyzer",
    "GrangerResult",
    "CausalityNetwork",
    "granger_causality_test",
    # Transfer Entropy
    "TransferEntropyAnalyzer",
    "TransferEntropyResult",
    "InformationFlowNetwork",
    "transfer_entropy",
    # Connectedness
    "ConnectednessAnalyzer",
    "ConnectednessResult",
    "DynamicConnectedness",
    "calculate_centrality",
    "identify_key_transmitters",
]
