#!/usr/bin/env python
"""
Update VIX regime data to include 2007-2026 (extended range).
This enables backtesting on 2008 Financial Crisis and other historical events.
"""

import yfinance as yf
import pandas as pd
import json
from datetime import datetime


def get_regime(vix_close: float) -> str:
    """Classify VIX level into regime."""
    if vix_close < 15:
        return "low_volatility"
    elif vix_close < 25:
        return "normal"
    elif vix_close < 35:
        return "elevated"
    else:
        return "high_volatility"


def main():
    print("Downloading VIX data from 2007...")
    vix = yf.download('^VIX', start='2007-01-01', end='2026-02-01', progress=False)
    
    # Fix multi-level columns if present
    if isinstance(vix.columns, pd.MultiIndex):
        vix.columns = vix.columns.get_level_values(0)
    
    print(f"Downloaded {len(vix)} trading days")
    
    # Build daily data
    daily_data = []
    for date, row in vix.iterrows():
        close = float(row['Close'])
        daily_data.append({
            "date": date.strftime("%Y-%m-%d"),
            "open": float(row['Open']),
            "high": float(row['High']),
            "low": float(row['Low']),
            "close": close,
            "regime": get_regime(close)
        })
    
    # Calculate regime distribution
    regimes = pd.Series([d['regime'] for d in daily_data]).value_counts()
    print("\nRegime Distribution (2007-2026):")
    for regime, count in regimes.items():
        pct = count / len(daily_data) * 100
        print(f"  {regime}: {count} days ({pct:.1f}%)")
    
    # Key events check
    print("\nKey Historical Events:")
    events = [
        ("2008 Financial Crisis Peak", "2008-11-20"),
        ("Flash Crash", "2010-05-06"),
        ("2011 Debt Ceiling", "2011-08-08"),
        ("2015 China Devaluation", "2015-08-24"),
        ("COVID Crash", "2020-03-16"),
        ("GameStop Peak", "2021-01-27"),
    ]
    
    vix_dict = {d['date']: d for d in daily_data}
    for name, date in events:
        if date in vix_dict:
            d = vix_dict[date]
            print(f"  {name} ({date}): VIX={d['close']:.1f} ({d['regime']})")
        else:
            print(f"  {name} ({date}): No data")
    
    # Save extended data
    output = {
        "metadata": {
            "start_date": daily_data[0]["date"],
            "end_date": daily_data[-1]["date"],
            "total_days": len(daily_data),
            "thresholds": {
                "low_volatility": "<15",
                "normal": "15-25",
                "elevated": "25-35",
                "high_volatility": "≥35"
            }
        },
        "daily_data": daily_data
    }
    
    output_path = "data/processed/vix_regimes_extended.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nSaved to {output_path}")
    print(f"Total days: {len(daily_data)}")


if __name__ == "__main__":
    main()
