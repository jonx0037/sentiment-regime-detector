#!/usr/bin/env python3
"""
Import COVID World Indices data.

This script imports 46 global market indices covering the COVID pandemic period
and beyond. Data is useful for:
1. Cross-market regime analysis
2. GARCH-MIDAS volatility features
3. Backtesting validation across global markets

Source: Kaggle COVID World Indices Dataset
Data Range: ~2010-2024 (varies by index)
"""

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sentiment_detector.models import Base, MarketData
from sentiment_detector.core.config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Default data path
DEFAULT_DATA_PATH = Path(__file__).parent.parent / "data" / "kaggle" / "covid-world-indices"

# Index metadata mapping (filename -> symbol, region, exchange)
INDEX_METADATA: Dict[str, Dict] = {
    "AEX": {"symbol": "^AEX", "region": "eu", "exchange": "AMS"},
    "ATX": {"symbol": "^ATX", "region": "eu", "exchange": "VIE"},
    "BEL-20": {"symbol": "^BFX", "region": "eu", "exchange": "BRU"},
    "BIST-100": {"symbol": "XU100.IS", "region": "eu", "exchange": "IST"},
    "BSE-Sensex": {"symbol": "^BSESN", "region": "in", "exchange": "BSE"},
    "Bovespa": {"symbol": "^BVSP", "region": "br", "exchange": "SAO"},
    "Budapest-SE": {"symbol": "^BUX", "region": "eu", "exchange": "BUD"},
    "CAC-40": {"symbol": "^FCHI", "region": "eu", "exchange": "PAR"},
    "CSE-All-Share": {"symbol": "^CSE", "region": "lk", "exchange": "CSE"},
    "China-A50": {"symbol": "^XIN9", "region": "cn", "exchange": "SSE"},
    "DAX": {"symbol": "^GDAXI", "region": "eu", "exchange": "FRA"},
    "DJ-New-Zealand": {"symbol": "^NZ50", "region": "nz", "exchange": "NZX"},
    "DJ-Shanghai": {"symbol": "^DJSH", "region": "cn", "exchange": "SSE"},
    "Dow-30": {"symbol": "^DJI", "region": "us", "exchange": "NYSE"},
    "Euro-Stoxx-50": {"symbol": "^STOXX50E", "region": "eu", "exchange": "STOXX"},
    "FTSE-100": {"symbol": "^FTSE", "region": "uk", "exchange": "LSE"},
    "FTSE-MIB": {"symbol": "FTSEMIB.MI", "region": "eu", "exchange": "MIL"},
    "HNX-30": {"symbol": "^HNX30", "region": "vn", "exchange": "HNX"},
    "Hang-Seng": {"symbol": "^HSI", "region": "hk", "exchange": "HKG"},
    "IBEX-35": {"symbol": "^IBEX", "region": "eu", "exchange": "MAD"},
    "IDX-Composite": {"symbol": "^JKSE", "region": "id", "exchange": "IDX"},
    "KOSPI-Composite": {"symbol": "^KS11", "region": "kr", "exchange": "KRX"},
    "MERVAL": {"symbol": "^MERV", "region": "ar", "exchange": "BCBA"},
    "Moex-Russia": {"symbol": "IMOEX.ME", "region": "ru", "exchange": "MOEX"},
    "Nasdaq": {"symbol": "^IXIC", "region": "us", "exchange": "NASDAQ"},
    "Nifty-50": {"symbol": "^NSEI", "region": "in", "exchange": "NSE"},
    "Nikkei-225": {"symbol": "^N225", "region": "jp", "exchange": "TYO"},
    "OMX-Copenhagen": {"symbol": "^OMXC25", "region": "eu", "exchange": "CPH"},
    "OMX-Helsinki": {"symbol": "^OMXH25", "region": "eu", "exchange": "HEL"},
    "OMX-Stockholm": {"symbol": "^OMXS30", "region": "eu", "exchange": "STO"},
    "Oslo-OBX": {"symbol": "^OBX", "region": "eu", "exchange": "OSL"},
    "PSI-20": {"symbol": "^PSI20", "region": "eu", "exchange": "LIS"},
    "QE": {"symbol": "^QSI", "region": "qa", "exchange": "QSE"},
    "Russell-2000": {"symbol": "^RUT", "region": "us", "exchange": "NYSE"},
    "S&P-500": {"symbol": "^GSPC", "region": "us", "exchange": "NYSE"},
    "S&P-ASX-200": {"symbol": "^AXJO", "region": "au", "exchange": "ASX"},
    "S&P-TSX": {"symbol": "^GSPTSE", "region": "ca", "exchange": "TSX"},
    "SMI": {"symbol": "^SSMI", "region": "ch", "exchange": "SWX"},
    "SET": {"symbol": "^SET.BK", "region": "th", "exchange": "SET"},
    "Shanghai-Composite": {"symbol": "^SSEC", "region": "cn", "exchange": "SSE"},
    "Shenzhen-Component": {"symbol": "^SZSC", "region": "cn", "exchange": "SZSE"},
    "TAIEX": {"symbol": "^TWII", "region": "tw", "exchange": "TWSE"},
    "TA-35": {"symbol": "^TA35", "region": "il", "exchange": "TASE"},
    "VN-Index": {"symbol": "^VNINDEX", "region": "vn", "exchange": "HOSE"},
    "WIG-20": {"symbol": "^WIG20", "region": "eu", "exchange": "WSE"},
}


def load_index_file(file_path: Path) -> Optional[pd.DataFrame]:
    """
    Load a single index CSV file.
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        DataFrame with OHLCV data or None if loading fails
    """
    try:
        df = pd.read_csv(file_path)
        
        # Standardize column names
        df.columns = [col.lower().replace(" ", "_") for col in df.columns]
        
        # Parse date
        df["date"] = pd.to_datetime(df["date"])
        
        # Extract index name from filename
        index_name = file_path.stem
        
        # Get metadata
        metadata = INDEX_METADATA.get(index_name, {
            "symbol": f"^{index_name.upper().replace('-', '')}",
            "region": "unknown",
            "exchange": "unknown"
        })
        
        df["symbol"] = metadata["symbol"]
        df["region"] = metadata["region"]
        df["exchange"] = metadata["exchange"]
        df["source_file"] = index_name
        
        return df
        
    except Exception as e:
        logger.error(f"Error loading {file_path}: {e}")
        return None


def load_all_indices(data_path: Path) -> pd.DataFrame:
    """
    Load all index CSV files from the data directory.
    
    Args:
        data_path: Path to the COVID indices directory
        
    Returns:
        Combined DataFrame with all indices
    """
    csv_files = list(data_path.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {data_path}")
    
    logger.info(f"Found {len(csv_files)} index files")
    
    all_dfs = []
    for csv_file in csv_files:
        df = load_index_file(csv_file)
        if df is not None:
            all_dfs.append(df)
            logger.info(f"  Loaded {csv_file.stem}: {len(df)} rows")
    
    if not all_dfs:
        raise ValueError("No data could be loaded")
    
    combined = pd.concat(all_dfs, ignore_index=True)
    
    logger.info(f"\nTotal: {len(combined)} observations across {len(all_dfs)} indices")
    logger.info(f"Date range: {combined['date'].min()} to {combined['date'].max()}")
    
    return combined


def calculate_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily returns for each index.
    
    Args:
        df: DataFrame with OHLCV data
        
    Returns:
        DataFrame with added daily_return column
    """
    df = df.sort_values(["symbol", "date"]).copy()
    df["daily_return"] = df.groupby("symbol")["close"].pct_change()
    return df


def analyze_indices(df: pd.DataFrame) -> dict:
    """
    Analyze the indices data for summary statistics.
    
    Returns:
        Dictionary with analysis results
    """
    analysis = {
        "total_observations": len(df),
        "num_indices": df["symbol"].nunique(),
        "date_range": {
            "start": df["date"].min(),
            "end": df["date"].max(),
        },
        "regions": df["region"].value_counts().to_dict(),
    }
    
    # Top indices by data availability
    index_counts = df.groupby("symbol").size().sort_values(ascending=False)
    analysis["top_indices"] = index_counts.head(10).to_dict()
    
    # Key crisis periods coverage
    crisis_periods = {
        "COVID Crash (Feb-Mar 2020)": ("2020-02-15", "2020-03-31"),
        "COVID Recovery (Apr-Dec 2020)": ("2020-04-01", "2020-12-31"),
        "2022 Drawdown (Jan-Oct 2022)": ("2022-01-01", "2022-10-31"),
    }
    
    coverage = {}
    for period_name, (start, end) in crisis_periods.items():
        period_data = df[(df["date"] >= start) & (df["date"] <= end)]
        coverage[period_name] = {
            "observations": len(period_data),
            "indices": period_data["symbol"].nunique(),
        }
    analysis["crisis_coverage"] = coverage
    
    return analysis


def import_to_database(
    df: pd.DataFrame,
    db_url: str,
    source: str = "covid_indices",
    batch_size: int = 5000,
    dry_run: bool = False,
) -> int:
    """
    Import market data to PostgreSQL database.
    
    Args:
        df: DataFrame with market data
        db_url: Database connection URL
        source: Source identifier
        batch_size: Number of records per batch
        dry_run: If True, don't actually insert data
        
    Returns:
        Number of records imported
    """
    if dry_run:
        logger.info("DRY RUN - No data will be imported")
        return 0
    
    engine = create_engine(db_url)
    
    # Create tables if they don't exist
    Base.metadata.create_all(engine)
    
    imported = 0
    
    with Session(engine) as session:
        # Check for existing data
        existing_count = session.execute(
            text("SELECT COUNT(*) FROM market_data WHERE source = :source"),
            {"source": source}
        ).scalar()
        
        if existing_count > 0:
            logger.warning(f"Found {existing_count} existing records for source '{source}'")
            user_input = input("Delete existing data and reimport? [y/N]: ")
            if user_input.lower() == "y":
                session.execute(
                    text("DELETE FROM market_data WHERE source = :source"),
                    {"source": source}
                )
                session.commit()
                logger.info(f"Deleted {existing_count} existing records")
            else:
                logger.info("Aborting import")
                return 0
        
        # Calculate returns before import
        df = calculate_returns(df)
        
        # Import in batches
        records = []
        for _, row in df.iterrows():
            record = MarketData(
                symbol=row["symbol"],
                asset_type="index",
                exchange=row.get("exchange"),
                region=row.get("region"),
                date=row["date"].date(),
                open=row.get("open"),
                high=row.get("high"),
                low=row.get("low"),
                close=row["close"],
                adj_close=row.get("adj_close"),
                volume=int(row["volume"]) if pd.notna(row.get("volume")) else None,
                daily_return=row.get("daily_return"),
                source=source,
            )
            records.append(record)
            
            if len(records) >= batch_size:
                session.add_all(records)
                session.commit()
                imported += len(records)
                logger.info(f"Imported {imported} records...")
                records = []
        
        # Import remaining records
        if records:
            session.add_all(records)
            session.commit()
            imported += len(records)
    
    logger.info(f"Successfully imported {imported} market data records")
    return imported


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Import COVID World Indices data to database"
    )
    parser.add_argument(
        "--data-path",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to COVID indices data directory",
    )
    parser.add_argument(
        "--db-url",
        type=str,
        default=None,
        help="Database URL (defaults to settings)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Analyze data without importing",
    )
    parser.add_argument(
        "--analyze-only",
        action="store_true",
        help="Only analyze the data",
    )
    parser.add_argument(
        "--indices",
        type=str,
        nargs="+",
        default=None,
        help="Specific indices to import (by filename stem)",
    )
    
    args = parser.parse_args()
    
    # Load data
    df = load_all_indices(args.data_path)
    
    # Filter indices if specified
    if args.indices:
        df = df[df["source_file"].isin(args.indices)]
        logger.info(f"Filtered to {len(df)} observations for specified indices")
    
    # Analyze data
    logger.info("\n" + "=" * 60)
    logger.info("COVID World Indices Analysis")
    logger.info("=" * 60)
    
    analysis = analyze_indices(df)
    
    logger.info(f"Total observations: {analysis['total_observations']:,}")
    logger.info(f"Number of indices: {analysis['num_indices']}")
    logger.info(f"Date range: {analysis['date_range']['start']} to {analysis['date_range']['end']}")
    
    logger.info("\nRegion distribution:")
    for region, count in sorted(analysis["regions"].items(), key=lambda x: -x[1]):
        logger.info(f"  {region}: {count:,}")
    
    logger.info("\nTop 10 indices by data availability:")
    for symbol, count in analysis["top_indices"].items():
        logger.info(f"  {symbol}: {count:,} observations")
    
    logger.info("\nCrisis period coverage:")
    for period, stats in analysis["crisis_coverage"].items():
        logger.info(f"  {period}: {stats['observations']:,} obs across {stats['indices']} indices")
    
    if args.analyze_only:
        return
    
    # Import to database
    db_url = args.db_url
    if not db_url:
        try:
            settings = get_settings()
            # Convert to string and use sync driver
            db_url = str(settings.database_url).replace("+asyncpg", "+psycopg2")
        except Exception as e:
            logger.error(f"Could not get database URL from settings: {e}")
            logger.info("Use --db-url to specify database connection")
            return
    
    import_to_database(df, db_url, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
