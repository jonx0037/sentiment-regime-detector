"""
Validation module for hypothesis testing and model evaluation.
"""

from .hypothesis_validator import (
    HypothesisValidator,
    HypothesisResult,
    H1Result,
    H2Result,
    H3Result,
    LeadLagResult,
    GrangerResult,
    generate_hypothesis_report,
)

from .walk_forward_backtest import (
    WalkForwardBacktester,
    WalkForwardResult,
    WindowResult,
    BacktestWindow,
    EventBacktestResult,
    MarketEvent,
    COVID_CRASH,
    GAMESTOP_SQUEEZE,
    CRYPTO_WINTER_2022,
    FTX_COLLAPSE,
    SVB_COLLAPSE,
    KEY_MARKET_EVENTS,
    create_synthetic_crisis_data,
)

__all__ = [
    # Hypothesis validation
    "HypothesisValidator",
    "HypothesisResult",
    "H1Result",
    "H2Result",
    "H3Result",
    "LeadLagResult",
    "GrangerResult",
    "generate_hypothesis_report",
    # Walk-forward backtesting
    "WalkForwardBacktester",
    "WalkForwardResult",
    "WindowResult",
    "BacktestWindow",
    "EventBacktestResult",
    "MarketEvent",
    "COVID_CRASH",
    "GAMESTOP_SQUEEZE",
    "CRYPTO_WINTER_2022",
    "FTX_COLLAPSE",
    "SVB_COLLAPSE",
    "KEY_MARKET_EVENTS",
    "create_synthetic_crisis_data",
]
