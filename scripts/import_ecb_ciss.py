#!/usr/bin/env python3
"""
Import ECB CISS (Composite Indicator of Systemic Stress) data.

This script imports ECB CISS data which serves dual purposes:
1. Ground truth for regime validation (known crisis periods)
2. Low-frequency feature for GARCH-MIDAS model

Source: ECB Statistical Data Warehouse
Data Range: 1980-2026 (daily)
"""

import argparse
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sentiment_detector.models import Base, StressIndex
from sentiment_detector.core.config import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Default data path
DEFAULT_DATA_PATH = Path(__file__).parent.parent / "data" / "kaggle" / "ecb-ciss"

# ECB CISS thresholds
HIGH_STRESS_THRESHOLD = 0.35
CRISIS_THRESHOLD = 0.50


def load_ecb_ciss_data(data_path: Path) -> pd.DataFrame:
    """
    Load ECB CISS data from CSV file.
    
    Args:
        data_path: Path to the ECB CISS data directory
        
    Returns:
        DataFrame with date and CISS value columns
    """
    # Find the CSV file
    csv_files = list(data_path.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {data_path}")
    
    csv_file = csv_files[0]
    logger.info(f"Loading ECB CISS data from {csv_file}")
    
    # Read CSV with proper column handling
    df = pd.read_csv(csv_file)
    
    # Rename columns for clarity
    df.columns = ["date", "date_label", "ciss_value"]
    
    # Parse date
    df["date"] = pd.to_datetime(df["date"])
    
    # Convert CISS value to float (handle any string issues)
    df["ciss_value"] = pd.to_numeric(df["ciss_value"], errors="coerce")
    
    # Drop rows with missing values
    initial_count = len(df)
    df = df.dropna(subset=["ciss_value"])
    dropped = initial_count - len(df)
    if dropped > 0:
        logger.warning(f"Dropped {dropped} rows with missing CISS values")
    
    logger.info(f"Loaded {len(df)} CISS observations")
    logger.info(f"Date range: {df['date'].min()} to {df['date'].max()}")
    
    return df


def analyze_crisis_periods(df: pd.DataFrame) -> dict:
    """
    Identify crisis periods based on CISS thresholds.
    
    Returns:
        Dictionary with crisis analysis
    """
    high_stress = df[df["ciss_value"] >= HIGH_STRESS_THRESHOLD]
    crisis = df[df["ciss_value"] >= CRISIS_THRESHOLD]
    
    analysis = {
        "total_observations": len(df),
        "high_stress_days": len(high_stress),
        "crisis_days": len(crisis),
        "high_stress_pct": len(high_stress) / len(df) * 100,
        "crisis_pct": len(crisis) / len(df) * 100,
        "max_ciss": df["ciss_value"].max(),
        "max_ciss_date": df.loc[df["ciss_value"].idxmax(), "date"],
        "mean_ciss": df["ciss_value"].mean(),
        "median_ciss": df["ciss_value"].median(),
    }
    
    # Identify major crisis periods (consecutive high stress days)
    df_sorted = df.sort_values("date").copy()
    df_sorted["is_crisis"] = df_sorted["ciss_value"] >= CRISIS_THRESHOLD
    df_sorted["crisis_group"] = (
        (df_sorted["is_crisis"] != df_sorted["is_crisis"].shift()).cumsum()
    )
    
    crisis_periods = []
    for group_id, group in df_sorted[df_sorted["is_crisis"]].groupby("crisis_group"):
        if len(group) >= 5:  # At least 5 consecutive crisis days
            crisis_periods.append({
                "start": group["date"].min(),
                "end": group["date"].max(),
                "duration_days": len(group),
                "max_ciss": group["ciss_value"].max(),
            })
    
    analysis["major_crisis_periods"] = crisis_periods
    
    return analysis


def import_to_database(
    df: pd.DataFrame,
    db_url: str,
    source: str = "ecb_ciss",
    region: str = "ea",
    batch_size: int = 1000,
    dry_run: bool = False,
) -> int:
    """
    Import CISS data to PostgreSQL database.
    
    Args:
        df: DataFrame with CISS data
        db_url: Database connection URL
        source: Source identifier
        region: Geographic region code
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
            text("SELECT COUNT(*) FROM stress_indices WHERE source = :source"),
            {"source": source}
        ).scalar()
        
        if existing_count > 0:
            logger.warning(f"Found {existing_count} existing records for source '{source}'")
            user_input = input("Delete existing data and reimport? [y/N]: ")
            if user_input.lower() == "y":
                session.execute(
                    text("DELETE FROM stress_indices WHERE source = :source"),
                    {"source": source}
                )
                session.commit()
                logger.info(f"Deleted {existing_count} existing records")
            else:
                logger.info("Aborting import")
                return 0
        
        # Import in batches
        records = []
        for _, row in df.iterrows():
            record = StressIndex(
                source=source,
                date=row["date"].date(),
                region=region,
                value=float(row["ciss_value"]),
                frequency="daily",
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
    
    logger.info(f"Successfully imported {imported} CISS records")
    return imported


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Import ECB CISS data to database"
    )
    parser.add_argument(
        "--data-path",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help="Path to ECB CISS data directory",
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
        help="Only analyze crisis periods",
    )
    
    args = parser.parse_args()
    
    # Load data
    df = load_ecb_ciss_data(args.data_path)
    
    # Analyze crisis periods
    logger.info("\n" + "=" * 60)
    logger.info("ECB CISS Crisis Analysis")
    logger.info("=" * 60)
    
    analysis = analyze_crisis_periods(df)
    
    logger.info(f"Total observations: {analysis['total_observations']:,}")
    logger.info(f"High stress days (CISS >= {HIGH_STRESS_THRESHOLD}): {analysis['high_stress_days']:,} ({analysis['high_stress_pct']:.1f}%)")
    logger.info(f"Crisis days (CISS >= {CRISIS_THRESHOLD}): {analysis['crisis_days']:,} ({analysis['crisis_pct']:.1f}%)")
    logger.info(f"Max CISS: {analysis['max_ciss']:.4f} on {analysis['max_ciss_date']}")
    logger.info(f"Mean CISS: {analysis['mean_ciss']:.4f}")
    logger.info(f"Median CISS: {analysis['median_ciss']:.4f}")
    
    logger.info("\nMajor Crisis Periods:")
    for period in analysis["major_crisis_periods"]:
        logger.info(
            f"  {period['start'].date()} to {period['end'].date()} "
            f"({period['duration_days']} days, max CISS: {period['max_ciss']:.4f})"
        )
    
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
