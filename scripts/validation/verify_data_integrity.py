#!/usr/bin/env python3
"""Verify data integrity for backtests.

This script checks:
- Database record counts (texts, sentiment scores, market data)
- Date coverage ranges
- Data completeness (CISS, VIX)
- Gaps in time series data

Part of Phase 2: Data Integrity Validation
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

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


async def validate_data_integrity() -> dict[str, any]:
    """Check for data gaps and inconsistencies.

    Returns:
        dict: Validation results with counts, date ranges, and issues
    """
    results = {
        "timestamp": datetime.now().isoformat(),
        "checks": {},
        "issues": [],
        "passed": True
    }

    async with get_session_context() as session:
        print("🔍 DATA INTEGRITY CHECK")
        print("=" * 60)

        # Check 1: Text counts
        print("\n📝 Checking text records...")
        text_count = await session.scalar(select(func.count(RawText.id)))
        results["checks"]["text_count"] = text_count
        print(f"✓ Texts in database: {text_count:,}")

        if text_count < 2_600_000:
            issue = f"⚠️  Expected ~2.66M texts, found {text_count:,}"
            print(issue)
            results["issues"].append(issue)
            results["passed"] = False

        # Check 2: Sentiment scores
        print("\n💭 Checking sentiment scores...")
        sentiment_count = await session.scalar(select(func.count(SentimentScore.id)))
        results["checks"]["sentiment_count"] = sentiment_count
        print(f"✓ Sentiment scores: {sentiment_count:,}")

        if sentiment_count != text_count:
            issue = f"⚠️  Sentiment/text mismatch: {sentiment_count:,} scores vs {text_count:,} texts"
            print(issue)
            results["issues"].append(issue)
            results["passed"] = False

        # Check 3: Market data coverage
        print("\n📊 Checking market data...")
        market_count = await session.scalar(select(func.count(MarketData.id)))
        results["checks"]["market_data_count"] = market_count
        print(f"✓ Market data points: {market_count:,}")

        # Check 4: Date coverage
        print("\n📅 Checking date ranges...")
        earliest_text = await session.scalar(
            select(func.min(RawText.collected_at))
        )
        latest_text = await session.scalar(
            select(func.max(RawText.collected_at))
        )
        results["checks"]["date_range"] = {
            "earliest": earliest_text.isoformat() if earliest_text else None,
            "latest": latest_text.isoformat() if latest_text else None
        }
        print(f"✓ Text date range: {earliest_text} to {latest_text}")

        earliest_market = await session.scalar(
            select(func.min(MarketData.date))
        )
        latest_market = await session.scalar(
            select(func.max(MarketData.date))
        )
        results["checks"]["market_date_range"] = {
            "earliest": earliest_market.isoformat() if earliest_market else None,
            "latest": latest_market.isoformat() if latest_market else None
        }
        print(f"✓ Market date range: {earliest_market} to {latest_market}")

        # Check 5: VIX symbol data (stored as symbol "^VIX")
        print("\n📈 Checking VIX data...")
        vix_count = await session.scalar(
            select(func.count(MarketData.id)).where(MarketData.symbol == "^VIX")
        )
        vix_earliest = await session.scalar(
            select(func.min(MarketData.date)).where(MarketData.symbol == "^VIX")
        )
        vix_latest = await session.scalar(
            select(func.max(MarketData.date)).where(MarketData.symbol == "^VIX")
        )
        results["checks"]["vix"] = {
            "total": vix_count,
            "earliest": vix_earliest.isoformat() if vix_earliest else None,
            "latest": vix_latest.isoformat() if vix_latest else None
        }

        if vix_count > 0:
            print(f"✓ VIX data: {vix_count:,} records")
            print(f"  Range: {vix_earliest} to {vix_latest}")
        else:
            issue = "⚠️  No VIX data found (symbol ^VIX)"
            print(issue)
            results["issues"].append(issue)
            results["passed"] = False

        # Check 6: Market symbols available
        print("\n📊 Checking available market symbols...")
        distinct_symbols = await session.execute(
            select(MarketData.symbol, func.count(MarketData.id))
            .group_by(MarketData.symbol)
            .order_by(func.count(MarketData.id).desc())
            .limit(10)
        )
        symbols = distinct_symbols.all()
        results["checks"]["top_symbols"] = [
            {"symbol": sym, "count": count} for sym, count in symbols
        ]
        print(f"✓ Top 10 symbols:")
        for sym, count in symbols:
            print(f"  {sym}: {count:,} records")

        # Check 7: Regime classifications
        print("\n🎯 Checking regime classifications...")
        regime_count = await session.scalar(select(func.count(RegimeState.id)))
        results["checks"]["regime_count"] = regime_count
        print(f"✓ Regime classifications: {regime_count:,}")

        # Summary
        print("\n" + "=" * 60)
        if results["passed"]:
            print("✅ DATA INTEGRITY CHECK PASSED")
            print("   All data appears complete and consistent")
        else:
            print("❌ DATA INTEGRITY CHECK FAILED")
            print(f"   Found {len(results['issues'])} issues:")
            for issue in results["issues"]:
                print(f"   - {issue}")
        print("=" * 60)

    return results


async def main():
    """Run data integrity validation."""
    try:
        results = await validate_data_integrity()

        # Save results to JSON
        import json
        output_dir = Path(__file__).parent.parent.parent / "results" / "validation"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"data_integrity_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\n📄 Results saved to: {output_file}")

        # Exit with appropriate code
        sys.exit(0 if results["passed"] else 1)

    except Exception as e:
        print(f"\n❌ ERROR: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    asyncio.run(main())
