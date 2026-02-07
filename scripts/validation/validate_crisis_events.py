#!/usr/bin/env python3
"""Validate crisis event data alignment.

This script verifies that data exists for all critical crisis event dates:
- 2008 Financial Crisis
- COVID-19 Pandemic
- GameStop Short Squeeze

For each event, checks:
- Market data availability (VIX, CISS)
- Sentiment data availability
- Regime classifications

Part of Phase 2: Data Integrity Validation
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from sentiment_detector.core.database import get_session_context
from sentiment_detector.models import (
    MarketData,
    RawText,
    RegimeState,
    SentimentScore,
)


# Crisis event definitions from research
CRISIS_EVENTS = {
    "2008_financial_crisis": {
        "name": "2008 Financial Crisis",
        "start": "2008-09-15",  # Lehman Brothers collapse
        "peak": "2008-11-20",   # CISS peak
        "end": "2009-03-09",    # Market bottom
        "expected_ciss_peak": 0.9428,
        "expected_sentiment_beta": -0.776
    },
    "covid19_pandemic": {
        "name": "COVID-19 Pandemic",
        "start": "2020-02-24",  # Market starts falling
        "peak": "2020-03-16",   # VIX peak (82.69)
        "end": "2020-04-15",    # Recovery begins
        "expected_vix_peak": 82.69,
        "expected_vix_ciss_correlation": 0.922
    },
    "gamestop_squeeze": {
        "name": "GameStop Short Squeeze",
        "start": "2021-01-13",  # Initial surge
        "peak": "2021-01-27",   # Peak volatility
        "end": "2021-02-05",    # Stabilization
        "expected_ciss_max": 0.024,
        "expected_systemic": False  # Should NOT be classified as systemic
    }
}


async def check_date_data(
    session: AsyncSession,
    date: datetime,
    event_name: str,
    phase: str
) -> dict[str, any]:
    """Check if data exists for a specific date.

    Args:
        session: Database session
        date: Date to check
        event_name: Name of crisis event
        phase: Phase of event (start, peak, end)

    Returns:
        dict: Data availability results
    """
    result = {
        "date": date.isoformat(),
        "event": event_name,
        "phase": phase,
        "market_data": False,
        "sentiment_data": False,
        "regime_data": False,
        "vix": None,
        "ciss": None,
        "regime_label": None,
        "issues": []
    }

    # Check market data
    market = await session.scalar(
        select(MarketData).where(MarketData.date == date.date())
    )
    if market:
        result["market_data"] = True
        result["vix"] = float(market.vix) if market.vix else None
        result["ciss"] = float(market.ciss) if market.ciss else None

        if market.vix is None:
            result["issues"].append("VIX data missing")
        if market.ciss is None:
            result["issues"].append("CISS data missing")
    else:
        result["issues"].append("No market data for this date")

    # Check sentiment data (count texts on this day)
    sentiment_count = await session.scalar(
        select(func.count(RawText.id)).where(
            func.date(RawText.collected_at) == date.date()
        )
    )
    if sentiment_count and sentiment_count > 0:
        result["sentiment_data"] = True
        result["sentiment_count"] = sentiment_count
    else:
        result["issues"].append("No sentiment data for this date")

    # Check regime classification
    regime = await session.scalar(
        select(Regime).where(RegimeState.date == date.date())
    )
    if regime:
        result["regime_data"] = True
        result["regime_label"] = regime.label
    else:
        result["issues"].append("No regime classification for this date")

    return result


async def validate_event_data(event_key: str, event_info: dict) -> dict[str, any]:
    """Verify data exists for all phases of a crisis event.

    Args:
        event_key: Event identifier key
        event_info: Event configuration dict

    Returns:
        dict: Validation results for this event
    """
    print(f"\n{'=' * 60}")
    print(f"📊 {event_info['name']}")
    print(f"{'=' * 60}")

    results = {
        "event": event_info["name"],
        "event_key": event_key,
        "phases": {},
        "passed": True,
        "issues": []
    }

    async with get_session_context() as session:
        for phase in ["start", "peak", "end"]:
            date_str = event_info[phase]
            date = pd.to_datetime(date_str)

            print(f"\n{phase.upper()}: {date_str}")

            phase_result = await check_date_data(
                session, date, event_info["name"], phase
            )
            results["phases"][phase] = phase_result

            # Print status
            if phase_result["market_data"]:
                print(f"  ✓ Market data available")
                if phase_result["vix"] is not None:
                    print(f"    VIX: {phase_result['vix']:.2f}")
                if phase_result["ciss"] is not None:
                    print(f"    CISS: {phase_result['ciss']:.4f}")
            else:
                print(f"  ✗ Market data MISSING")
                results["passed"] = False

            if phase_result["sentiment_data"]:
                print(f"  ✓ Sentiment data available ({phase_result.get('sentiment_count', 0):,} texts)")
            else:
                print(f"  ✗ Sentiment data MISSING")
                results["passed"] = False

            if phase_result["regime_data"]:
                print(f"  ✓ Regime: {phase_result['regime_label']}")
            else:
                print(f"  ✗ Regime classification MISSING")
                results["passed"] = False

            # Track issues
            if phase_result["issues"]:
                for issue in phase_result["issues"]:
                    issue_str = f"{phase}: {issue}"
                    results["issues"].append(issue_str)
                    print(f"  ⚠️  {issue}")

        # Check expected values for peak
        if "peak" in results["phases"]:
            peak = results["phases"]["peak"]

            if "expected_vix_peak" in event_info and peak["vix"]:
                expected = event_info["expected_vix_peak"]
                actual = peak["vix"]
                diff_pct = abs(actual - expected) / expected * 100

                if diff_pct > 5:
                    issue = f"VIX peak differs by {diff_pct:.1f}% (expected {expected}, got {actual})"
                    results["issues"].append(issue)
                    print(f"\n  ⚠️  {issue}")

            if "expected_ciss_peak" in event_info and peak["ciss"]:
                expected = event_info["expected_ciss_peak"]
                actual = peak["ciss"]
                diff_pct = abs(actual - expected) / expected * 100

                if diff_pct > 5:
                    issue = f"CISS peak differs by {diff_pct:.1f}% (expected {expected}, got {actual})"
                    results["issues"].append(issue)
                    print(f"\n  ⚠️  {issue}")

    return results


async def main():
    """Run crisis event data validation."""
    print("🔍 CRISIS EVENT DATA VALIDATION")
    print("=" * 60)
    print("Validating data availability for historical crisis events")

    all_results = {
        "timestamp": datetime.now().isoformat(),
        "events": {},
        "overall_passed": True
    }

    try:
        for event_key, event_info in CRISIS_EVENTS.items():
            result = await validate_event_data(event_key, event_info)
            all_results["events"][event_key] = result

            if not result["passed"]:
                all_results["overall_passed"] = False

        # Summary
        print("\n" + "=" * 60)
        print("📋 VALIDATION SUMMARY")
        print("=" * 60)

        for event_key, result in all_results["events"].items():
            status = "✅ PASSED" if result["passed"] else "❌ FAILED"
            print(f"\n{result['event']}: {status}")
            if result["issues"]:
                print(f"  Issues found: {len(result['issues'])}")
                for issue in result["issues"][:3]:  # Show first 3
                    print(f"    - {issue}")
                if len(result["issues"]) > 3:
                    print(f"    ... and {len(result['issues']) - 3} more")

        print("\n" + "=" * 60)
        if all_results["overall_passed"]:
            print("✅ ALL CRISIS EVENTS VALIDATED")
        else:
            print("❌ VALIDATION FAILED FOR SOME EVENTS")
        print("=" * 60)

        # Save results
        import json
        output_dir = Path(__file__).parent.parent.parent / "results" / "validation"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"crisis_events_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, "w") as f:
            json.dump(all_results, f, indent=2)

        print(f"\n📄 Results saved to: {output_file}")

        # Exit with appropriate code
        sys.exit(0 if all_results["overall_passed"] else 1)

    except Exception as e:
        print(f"\n❌ ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    asyncio.run(main())
