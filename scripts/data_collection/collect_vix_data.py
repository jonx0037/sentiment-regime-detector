#!/usr/bin/env python3
"""
Collect VIX data for regime ground truth.

VIX levels define market regimes:
- Low volatility: VIX < 15 (bullish/calm)
- Normal: 15 <= VIX < 25
- Elevated: 25 <= VIX < 35
- High volatility: VIX >= 35 (crisis/panic)

Per Dakalbab et al. (2024), VIX serves as ground truth
for regime classification evaluation.
"""

import argparse
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pandas as pd
from sentiment_detector.collectors.market_data import MarketDataCollector

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def classify_vix_regime(vix_level: float) -> str:
    """
    Classify VIX level into regime category.
    
    Args:
        vix_level: VIX closing value
        
    Returns:
        Regime classification string
    """
    if vix_level < 15:
        return "low_volatility"
    elif vix_level < 25:
        return "normal"
    elif vix_level < 35:
        return "elevated"
    else:
        return "high_volatility"


def collect_vix_data(
    start_date: str,
    end_date: str,
    output_path: Path
) -> None:
    """
    Collect VIX data and classify into regimes.
    
    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        output_path: Output file path
    """
    logger.info(f"Collecting VIX data from {start_date} to {end_date}")
    
    collector = MarketDataCollector()
    
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    # Get VIX data
    vix_df = collector.get_vix(start, end)
    
    if vix_df.empty:
        logger.error("No VIX data retrieved")
        return
    
    logger.info(f"Retrieved {len(vix_df)} VIX data points")
    
    # Process data
    records = []
    
    for date, row in vix_df.iterrows():
        if hasattr(row, 'Close'):
            close = row['Close']
        else:
            close = row.get(('Close', '^VIX'), row.iloc[3] if len(row) > 3 else None)
        
        if pd.notna(close):
            regime = classify_vix_regime(float(close))
            records.append({
                "date": date.strftime("%Y-%m-%d"),
                "vix_close": float(close),
                "vix_open": float(row.get('Open', row.iloc[0])) if pd.notna(row.get('Open', row.iloc[0] if len(row) > 0 else None)) else None,
                "vix_high": float(row.get('High', row.iloc[1])) if pd.notna(row.get('High', row.iloc[1] if len(row) > 1 else None)) else None,
                "vix_low": float(row.get('Low', row.iloc[2])) if pd.notna(row.get('Low', row.iloc[2] if len(row) > 2 else None)) else None,
                "regime": regime
            })
    
    # Calculate regime statistics
    regime_counts = {}
    for r in records:
        regime_counts[r["regime"]] = regime_counts.get(r["regime"], 0) + 1
    
    # Save results
    output = {
        "metadata": {
            "start_date": start_date,
            "end_date": end_date,
            "total_days": len(records),
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "regime_distribution": regime_counts,
        "daily_data": records
    }
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    
    logger.info(f"Saved VIX data to {output_path}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("VIX DATA COLLECTION SUMMARY")
    print("=" * 60)
    print(f"Date Range: {start_date} to {end_date}")
    print(f"Total Trading Days: {len(records)}")
    print("\nRegime Distribution:")
    for regime, count in sorted(regime_counts.items()):
        pct = count / len(records) * 100
        print(f"  {regime:20}: {count:5} ({pct:5.1f}%)")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Collect VIX data for regime ground truth")
    parser.add_argument(
        "--start-date",
        type=str,
        default="2015-01-01",
        help="Start date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--end-date",
        type=str,
        default="2024-12-31",
        help="End date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/processed/vix_regimes.json",
        help="Output JSON file path"
    )
    
    args = parser.parse_args()
    
    collect_vix_data(
        start_date=args.start_date,
        end_date=args.end_date,
        output_path=Path(args.output)
    )


if __name__ == "__main__":
    main()
