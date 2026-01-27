#!/usr/bin/env python3
"""
Test MarketDataCollector functionality.

Verifies:
- yfinance connection
- VIX data retrieval
- Asset class price data
- Return and volatility calculations
"""

import sys
sys.path.insert(0, '/Users/jonathanrocha/Documents/SMU/DS_6210_Capstone/src')

from datetime import datetime, timedelta, timezone
from sentiment_detector.collectors.market_data import MarketDataCollector
from sentiment_detector.collectors.base import AssetClass


def test_health_check():
    """Test basic connectivity."""
    print("=" * 70)
    print("1. Testing yfinance connectivity...")
    print("=" * 70)
    
    collector = MarketDataCollector()
    is_healthy = collector.health_check()
    
    if is_healthy:
        print("✅ yfinance is working properly\n")
        return True
    else:
        print("❌ yfinance health check failed\n")
        return False


def test_current_vix():
    """Test current VIX retrieval."""
    print("=" * 70)
    print("2. Testing current VIX retrieval...")
    print("=" * 70)
    
    collector = MarketDataCollector()
    vix = collector.get_current_vix()
    
    if vix is not None:
        print(f"✅ Current VIX: {vix:.2f}")
        
        # Interpret VIX level
        if vix < 15:
            regime = "LOW (Market Complacency)"
        elif vix < 20:
            regime = "NORMAL (Moderate Volatility)"
        elif vix < 30:
            regime = "ELEVATED (Market Stress)"
        else:
            regime = "HIGH (Fear/Panic)"
        
        print(f"   Regime: {regime}\n")
        return True
    else:
        print("❌ Failed to retrieve current VIX\n")
        return False


def test_historical_vix():
    """Test historical VIX data."""
    print("=" * 70)
    print("3. Testing historical VIX data...")
    print("=" * 70)
    
    collector = MarketDataCollector()
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=30)
    
    vix_data = collector.get_vix(start_date, end_date)
    
    if not vix_data.empty:
        print(f"✅ Retrieved {len(vix_data)} days of VIX data")
        print(f"   Date Range: {vix_data.index[0]} to {vix_data.index[-1]}")
        
        # Handle multi-level or single-level columns
        if isinstance(vix_data.columns, pd.MultiIndex):
            close_data = vix_data[("^VIX", "Close")]
        else:
            close_data = vix_data["Close"]
        
        print(f"   VIX Range: {close_data.min():.2f} - {close_data.max():.2f}")
        print(f"   VIX Mean: {close_data.mean():.2f}")
        print(f"   VIX Std: {close_data.std():.2f}\n")
        return True
    else:
        print("❌ Failed to retrieve historical VIX\n")
        return False


def test_equity_prices():
    """Test equity price data."""
    print("=" * 70)
    print("4. Testing equity price data...")
    print("=" * 70)
    
    collector = MarketDataCollector()
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=7)
    
    prices = collector.get_asset_class_prices(
        AssetClass.EQUITY,
        start_date,
        end_date
    )
    
    if not prices.empty:
        print(f"✅ Retrieved equity prices")
        print(f"   Symbols: SPY, QQQ, IWM, DIA")
        print(f"   Data Points: {len(prices)} days")
        
        # Show latest SPY price if available
        if "SPY" in prices.columns.get_level_values(0):
            spy_close = prices["SPY"]["Close"].iloc[-1]
            print(f"   Latest SPY: ${spy_close:.2f}\n")
        return True
    else:
        print("❌ Failed to retrieve equity prices\n")
        return False


def test_crypto_prices():
    """Test crypto price data."""
    print("=" * 70)
    print("5. Testing crypto price data...")
    print("=" * 70)
    
    collector = MarketDataCollector()
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=7)
    
    prices = collector.get_asset_class_prices(
        AssetClass.CRYPTO,
        start_date,
        end_date
    )
    
    if not prices.empty:
        print(f"✅ Retrieved crypto prices")
        print(f"   Symbols: BTC-USD, ETH-USD, SOL-USD")
        print(f"   Data Points: {len(prices)} days")
        
        # Show latest BTC price if available
        if "BTC-USD" in prices.columns.get_level_values(0):
            btc_close = prices["BTC-USD"]["Close"].iloc[-1]
            print(f"   Latest BTC: ${btc_close:,.2f}\n")
        return True
    else:
        print("❌ Failed to retrieve crypto prices\n")
        return False


def test_volatility_calculation():
    """Test volatility calculation."""
    print("=" * 70)
    print("6. Testing volatility calculation...")
    print("=" * 70)
    
    collector = MarketDataCollector()
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=60)
    
    prices = collector.get_asset_class_prices(
        AssetClass.EQUITY,
        start_date,
        end_date
    )
    
    if not prices.empty:
        volatility = collector.calculate_volatility(prices, window=20)
        
        print("✅ Calculated 20-day rolling volatility")
        print("   Annualized volatility (latest):")
        
        # Show latest volatility for each symbol
        if hasattr(volatility, 'items'):
            for symbol in volatility.columns:
                latest_vol = volatility[symbol].iloc[-1]
                if not pd.isna(latest_vol):
                    print(f"   {symbol}: {latest_vol*100:.1f}%")
        print()
        return True
    else:
        print("❌ Failed to calculate volatility\n")
        return False


def test_returns_calculation():
    """Test returns calculation."""
    print("=" * 70)
    print("7. Testing returns calculation...")
    print("=" * 70)
    
    collector = MarketDataCollector()
    end_date = datetime.now(timezone.utc)
    start_date = end_date - timedelta(days=30)
    
    prices = collector.get_prices(
        symbols=["SPY"],
        start_date=start_date,
        end_date=end_date
    )
    
    if not prices.empty:
        returns = collector.calculate_returns(prices)
        
        # Handle both Series and DataFrame
        if hasattr(returns, 'columns') and len(returns.columns) > 0:
            # It's a DataFrame, get the first column
            returns_series = returns.iloc[:, 0]
        else:
            # It's already a Series
            returns_series = returns
        
        print("✅ Calculated daily returns for SPY")
        mean_return = returns_series.mean() * 100
        std_return = returns_series.std() * 100
        cum_return = (1 + returns_series).prod() - 1
        print(f"   Mean Daily Return: {mean_return:.3f}%")
        print(f"   Std Daily Return: {std_return:.3f}%")
        print(f"   Cumulative Return: {cum_return:.2%}\n")
        return True
    else:
        print("❌ Failed to calculate returns\n")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("MARKET DATA COLLECTOR - Comprehensive Test Suite")
    print("=" * 70)
    print()
    
    results = []
    
    # Run tests
    results.append(("Health Check", test_health_check()))
    results.append(("Current VIX", test_current_vix()))
    results.append(("Historical VIX", test_historical_vix()))
    results.append(("Equity Prices", test_equity_prices()))
    results.append(("Crypto Prices", test_crypto_prices()))
    results.append(("Volatility Calculation", test_volatility_calculation()))
    results.append(("Returns Calculation", test_returns_calculation()))
    
    # Summary
    print("=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:8} | {test_name}")
    
    print("=" * 70)
    print(f"Results: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    print("=" * 70)
    
    if passed == total:
        print("\n🎉 All tests passed! MarketDataCollector is fully functional.")
        print("\nNext steps:")
        print("  1. Build React Dashboard for visualization")
        print("  2. Request MANEFRAME access for model fine-tuning")
        print("  3. Implement regime classifier logic")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above.")
    
    print()


if __name__ == "__main__":
    import pandas as pd
    main()
