"""Historical crisis events for explainability analysis.

These events are used to demonstrate the model's explainability on known
market stress periods. Each event represents a significant market disruption
where regime classification is particularly important.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class CrisisEvent:
    """Historical crisis event metadata."""

    event_id: str
    name: str
    date: str  # YYYY-MM-DD format
    description: str
    ciss_peak: Optional[float] = None
    vix_peak: Optional[float] = None


# Historical crisis events for analysis
# Dates chosen to represent peak crisis periods
CRISIS_EVENTS = {
    "financial_crisis_2008": CrisisEvent(
        event_id="financial_crisis_2008",
        name="2008 Financial Crisis",
        date="2008-11-20",  # CISS peak period
        description=(
            "Global financial crisis triggered by subprime mortgage collapse. "
            "Peak systemic stress period with extreme market volatility."
        ),
        ciss_peak=0.98,  # Near maximum stress
        vix_peak=80.86,  # November 20, 2008
    ),
    "covid_crash_2020": CrisisEvent(
        event_id="covid_crash_2020",
        name="COVID-19 Market Crash",
        date="2020-03-16",  # VIX peak
        description=(
            "Pandemic-driven market crash with unprecedented volatility. "
            "Global risk-off sentiment across all asset classes."
        ),
        ciss_peak=0.66,
        vix_peak=82.69,  # Highest VIX since 2008
    ),
    "gamestop_2021": CrisisEvent(
        event_id="gamestop_2021",
        name="GameStop/Meme Stock Episode",
        date="2021-01-28",  # Peak retail trading day
        description=(
            "Retail-driven short squeeze creating localized stress. "
            "Divergence between equity sentiment and systemic indicators."
        ),
        ciss_peak=0.18,  # Low systemic stress
        vix_peak=37.21,  # Moderate volatility spike
    ),
    "luna_collapse_2022": CrisisEvent(
        event_id="luna_collapse_2022",
        name="Luna/Terra Collapse",
        date="2022-05-09",  # Luna depegging
        description=(
            "Algorithmic stablecoin collapse causing crypto-specific contagion. "
            "Test of cross-asset isolation vs. spillover effects."
        ),
        ciss_peak=0.48,  # Moderate systemic stress
        vix_peak=34.66,
    ),
    "celsius_3ac_2022": CrisisEvent(
        event_id="celsius_3ac_2022",
        name="Celsius/3AC Crypto Contagion",
        date="2022-06-15",  # Peak withdrawal stress
        description=(
            "Crypto lending platform failures and hedge fund liquidations. "
            "Crypto-specific stress with limited traditional market impact."
        ),
        ciss_peak=0.52,
        vix_peak=33.89,
    ),
    "out_of_sample_2024": CrisisEvent(
        event_id="out_of_sample_2024",
        name="Out-of-Sample Validation Period",
        date="2024-10-01",  # Representative date from validation period
        description=(
            "Out-of-sample period (2024-2026) for model validation. "
            "Tests generalization to unseen market conditions."
        ),
        ciss_peak=None,  # TBD based on actual data
        vix_peak=None,
    ),
}


def get_event(event_id: str) -> Optional[CrisisEvent]:
    """Get crisis event by ID.

    Args:
        event_id: Event identifier

    Returns:
        CrisisEvent if found, None otherwise
    """
    return CRISIS_EVENTS.get(event_id)


def list_events() -> list[CrisisEvent]:
    """Get all crisis events ordered chronologically.

    Returns:
        List of CrisisEvent objects sorted by date
    """
    return sorted(CRISIS_EVENTS.values(), key=lambda e: e.date)
