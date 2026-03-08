#!/usr/bin/env python3
"""Train a Random Forest regime classifier and save as pickle checkpoint.

Generates models/regime_classifier_rf.pkl for SHAP explainability.
Uses pickle for model serialization (trusted internal checkpoint only).

Usage:
    python scripts/train_regime_classifier.py --from-csv   # train from local CSV files
    python scripts/train_regime_classifier.py              # train from database
    python scripts/train_regime_classifier.py --dry-run    # validate without saving
"""

import sys
from pathlib import Path

# Add src to path so imports work when run as a script
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import argparse
import asyncio
import logging
import pickle  # nosec B403 — saving/loading trusted internal model checkpoints only
from datetime import datetime, timezone

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
DATA_DIR = Path(__file__).parent.parent / "data"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants – must match the 28 features expected by RegimeExplainer
# ---------------------------------------------------------------------------
FEATURE_NAMES = [
    # CISS (8)
    "ciss_lag1", "ciss_change", "ciss_change_5d",
    "ciss_ma5", "ciss_ma20", "ciss_above_ma20",
    "ciss_std_20d", "ciss_trend",
    # VIX (8)
    "vix", "vix_change", "vix_change_pct",
    "vix_ma5", "vix_ma20", "vix_above_ma20",
    "vix_spike", "vix_range",
    # Sentiment (9)
    "sentiment", "sentiment_change", "sentiment_momentum_5d",
    "sentiment_momentum_20d", "sentiment_ma5", "sentiment_ma20",
    "sentiment_acceleration", "sentiment_dispersion", "sentiment_spread",
    # Cross-asset (3)
    "cross_asset_divergence", "ciss_vix_ratio", "sentiment_vix_interaction",
]

LABEL_MAP = {"risk_on": 0, "transition": 1, "risk_off": 2}
INV_LABEL_MAP = {v: k for k, v in LABEL_MAP.items()}

# Rule-based thresholds (from RegimeClassifier in services/regime_classifier.py)
CISS_HIGH = 0.30   # elevated systemic stress
CISS_LOW = 0.10    # calm markets
VIX_HIGH = 25.0    # fear gauge elevated
VIX_LOW = 16.0     # complacency
SENT_NEG = -0.10   # negative sentiment
SENT_POS = 0.10    # positive sentiment


# ---------------------------------------------------------------------------
# Data fetching — CSV (default, no database needed)
# ---------------------------------------------------------------------------
def fetch_raw_data_from_csv() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load CISS, VIX, and sentiment time series from local CSV files."""
    # CISS
    ciss_path = DATA_DIR / "ecb_ciss_daily.csv"
    ciss_raw = pd.read_csv(ciss_path)
    ciss_df = pd.DataFrame({
        "date": pd.to_datetime(ciss_raw.iloc[:, 0]),
        "ciss": pd.to_numeric(ciss_raw.iloc[:, 2], errors="coerce"),
    }).dropna()
    logger.info(f"Loaded {len(ciss_df)} CISS rows from {ciss_path.name}")

    # VIX
    vix_path = DATA_DIR / "vix_daily.csv"
    vix_raw = pd.read_csv(vix_path)
    vix_df = pd.DataFrame({
        "date": pd.to_datetime(vix_raw["date"]),
        "vix": pd.to_numeric(vix_raw["close"], errors="coerce"),
    }).dropna()
    logger.info(f"Loaded {len(vix_df)} VIX rows from {vix_path.name}")

    # Sentiment
    sent_path = DATA_DIR / "ensemble_daily_sentiment.csv"
    sent_raw = pd.read_csv(sent_path)
    sent_df = pd.DataFrame({
        "date": pd.to_datetime(sent_raw["date"]),
        "sentiment": pd.to_numeric(sent_raw["ensemble_mean"], errors="coerce"),
    }).dropna()
    logger.info(f"Loaded {len(sent_df)} sentiment rows from {sent_path.name}")

    return ciss_df, vix_df, sent_df


# ---------------------------------------------------------------------------
# Data fetching — Database (requires running PostgreSQL)
# ---------------------------------------------------------------------------
async def fetch_raw_data_from_db() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Fetch CISS, VIX, and sentiment time series from the database."""
    from sqlalchemy import text
    from sentiment_detector.core.database import async_session_maker

    async with async_session_maker() as session:
        # CISS
        ciss_result = await session.execute(text(
            "SELECT date, value FROM stress_indices "
            "WHERE source = 'ecb_ciss' ORDER BY date"
        ))
        ciss_df = pd.DataFrame(ciss_result.fetchall(), columns=["date", "ciss"])
        ciss_df["date"] = pd.to_datetime(ciss_df["date"])
        logger.info(f"Fetched {len(ciss_df)} CISS rows")

        # VIX
        vix_result = await session.execute(text(
            "SELECT date, close FROM market_data "
            "WHERE symbol = '^VIX' ORDER BY date"
        ))
        vix_df = pd.DataFrame(vix_result.fetchall(), columns=["date", "vix"])
        vix_df["date"] = pd.to_datetime(vix_df["date"])
        logger.info(f"Fetched {len(vix_df)} VIX rows")

        # Sentiment (daily aggregates)
        sent_result = await session.execute(text(
            "SELECT period_start AS date, "
            "       AVG(mean_compound) AS sentiment "
            "FROM sentiment_indices "
            "WHERE source IS NULL "
            "GROUP BY period_start ORDER BY period_start"
        ))
        sent_df = pd.DataFrame(sent_result.fetchall(), columns=["date", "sentiment"])
        sent_df["date"] = pd.to_datetime(sent_df["date"])
        logger.info(f"Fetched {len(sent_df)} sentiment rows")

    return ciss_df, vix_df, sent_df


# ---------------------------------------------------------------------------
# Feature engineering  (mirrors build_feature_dict in explainability.py)
# ---------------------------------------------------------------------------
def engineer_features(
    ciss_df: pd.DataFrame,
    vix_df: pd.DataFrame,
    sent_df: pd.DataFrame,
) -> pd.DataFrame:
    """Compute the 28-feature matrix from raw time series."""
    # Merge on date (inner join keeps only dates with all three series)
    df = ciss_df.merge(vix_df, on="date", how="inner")
    df = df.merge(sent_df, on="date", how="inner")
    df = df.sort_values("date").reset_index(drop=True)
    logger.info(f"Merged dataset: {len(df)} rows")

    if len(df) < 25:
        raise RuntimeError(
            f"Need at least 25 rows for feature engineering, got {len(df)}. "
            "Populate stress_indices, market_data, and sentiment_indices first."
        )

    # --- CISS features ---
    df["ciss_lag1"] = df["ciss"].shift(1)
    df["ciss_change"] = df["ciss"] - df["ciss"].shift(1)
    df["ciss_change_5d"] = df["ciss"] - df["ciss"].shift(5)
    df["ciss_ma5"] = df["ciss"].rolling(5).mean()
    df["ciss_ma20"] = df["ciss"].rolling(20).mean()
    df["ciss_above_ma20"] = (df["ciss"] > df["ciss_ma20"]).astype(float)
    df["ciss_std_20d"] = df["ciss"].rolling(20).std()
    df["ciss_trend"] = np.sign(df["ciss"] - df["ciss"].shift(5))

    # --- VIX features ---
    df["vix_change"] = df["vix"] - df["vix"].shift(1)
    df["vix_change_pct"] = df["vix"].pct_change() * 100
    df["vix_ma5"] = df["vix"].rolling(5).mean()
    df["vix_ma20"] = df["vix"].rolling(20).mean()
    df["vix_above_ma20"] = (df["vix"] > df["vix_ma20"]).astype(float)
    df["vix_spike"] = (df["vix"] > df["vix_ma20"] * 1.2).astype(float)
    df["vix_range"] = df["vix"].rolling(20).max() - df["vix"].rolling(20).min()

    # --- Sentiment features ---
    df["sentiment_change"] = df["sentiment"] - df["sentiment"].shift(1)
    df["sentiment_ma5"] = df["sentiment"].rolling(5).mean()
    df["sentiment_ma20"] = df["sentiment"].rolling(20).mean()
    df["sentiment_momentum_5d"] = df["sentiment_ma5"] - df["sentiment"].rolling(10).apply(
        lambda x: x[5:].mean() if len(x) >= 10 else x.mean(), raw=False,
    )
    df["sentiment_momentum_20d"] = df["sentiment_ma5"] - df["sentiment_ma20"]
    df["sentiment_acceleration"] = df["sentiment_change"].diff()
    df["sentiment_dispersion"] = df["sentiment"].rolling(20).std()
    df["sentiment_spread"] = df["sentiment"] - df["sentiment_ma20"]

    # --- Cross-asset features ---
    df["cross_asset_divergence"] = df["sentiment_dispersion"]  # proxy
    df["ciss_vix_ratio"] = df["ciss"] / df["vix"].replace(0, np.nan)
    df["sentiment_vix_interaction"] = df["sentiment"] * df["vix"] / 100.0

    # Drop rows with NaN from rolling windows (first ~20 rows)
    df = df.dropna(subset=FEATURE_NAMES).reset_index(drop=True)
    logger.info(f"After feature engineering: {len(df)} usable rows")

    return df


# ---------------------------------------------------------------------------
# Label generation  (rule-based teacher)
# ---------------------------------------------------------------------------
def generate_labels(df: pd.DataFrame) -> pd.Series:
    """Assign regime labels using rule-based heuristics.

    Mirrors the logic in RegimeClassifier._calculate_probabilities()
    but operates on the feature DataFrame directly.
    """
    labels = pd.Series("transition", index=df.index)

    # Risk-off: high stress OR high VIX OR negative sentiment
    risk_off_mask = (
        (df["ciss_lag1"] > CISS_HIGH)
        | (df["vix"] > VIX_HIGH)
        | (df["sentiment"] < SENT_NEG)
    )

    # Risk-on: low stress AND low VIX AND positive sentiment
    risk_on_mask = (
        (df["ciss_lag1"] < CISS_LOW)
        & (df["vix"] < VIX_LOW)
        & (df["sentiment"] > SENT_POS)
    )

    labels[risk_off_mask] = "risk_off"
    labels[risk_on_mask] = "risk_on"

    counts = labels.value_counts()
    logger.info(f"Label distribution:\n{counts.to_string()}")

    return labels.map(LABEL_MAP)


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------
def train_model(
    X: pd.DataFrame,
    y: pd.Series,
    *,
    dry_run: bool = False,
) -> dict:
    """Train Random Forest and return checkpoint dict."""
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y,
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestClassifier(
        n_estimators=200,
        max_depth=10,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced",
    )
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(
        y_test, y_pred, target_names=list(LABEL_MAP.keys()), output_dict=True,
    )

    logger.info(f"Test accuracy: {accuracy:.4f}")
    logger.info(
        classification_report(y_test, y_pred, target_names=list(LABEL_MAP.keys()))
    )

    train_end_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    checkpoint = {
        "model": model,
        "scaler": scaler,
        "feature_names": list(X.columns),
        "label_map": LABEL_MAP,
        "model_type": "RandomForestClassifier",
        "model_version": f"RF_v{train_end_date[:4]}.{train_end_date[5:7]}",
        "train_end_date": train_end_date,
        "metrics": {
            "accuracy": accuracy,
            "classification_report": report,
            "n_train": len(X_train),
            "n_test": len(X_test),
        },
    }

    if dry_run:
        logger.info("Dry run — skipping model save")
    else:
        save_checkpoint(checkpoint)

    return checkpoint


def save_checkpoint(checkpoint: dict) -> Path:
    """Save checkpoint to models/regime_classifier_rf.pkl.

    Uses pickle for trusted internal model serialization (nosec B301).
    """
    output_dir = Path(__file__).parent.parent / "models"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "regime_classifier_rf.pkl"

    with open(output_path, "wb") as f:
        pickle.dump(checkpoint, f)  # nosec B301 — trusted internal checkpoint

    size_mb = output_path.stat().st_size / 1024 / 1024
    logger.info(f"Saved checkpoint to {output_path} ({size_mb:.1f} MB)")
    return output_path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Train regime classifier for SHAP explainability")
    parser.add_argument("--dry-run", action="store_true", help="Validate pipeline without saving")
    parser.add_argument("--from-csv", action="store_true", default=True,
                        help="Train from local CSV files (default)")
    parser.add_argument("--from-db", action="store_true",
                        help="Train from database (requires running PostgreSQL)")
    args = parser.parse_args()

    if args.from_db:
        logger.info("Loading data from database...")
        ciss_df, vix_df, sent_df = asyncio.run(fetch_raw_data_from_db())
    else:
        logger.info("Loading data from CSV files...")
        ciss_df, vix_df, sent_df = fetch_raw_data_from_csv()

    df = engineer_features(ciss_df, vix_df, sent_df)

    X = df[FEATURE_NAMES]
    y = generate_labels(df)

    train_model(X, y, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
