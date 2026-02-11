#!/usr/bin/env python3
"""
End-to-End Regime Detection Analysis.

Runs the full pipeline on daily_sentiment.csv + VIX + CISS + SPY market data.
Self-contained — no dependency on src/ package imports (runs on HPC).

Pipeline stages:
1. Data loading & alignment (sentiment already daily-aggregated)
2. Feature engineering (transfer entropy proxy, connectedness, momentum)
3. GARCH(1,1) volatility modeling
4. Statistical Jump Model regime classification
5. Export results (CSVs + JSON summary)
"""

import argparse
import json
import os
import sys
import time
import warnings
from datetime import datetime

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)


# ─── Configuration ────────────────────────────────────────────────

N_REGIMES = 4
JUMP_PENALTY = 5.0
MIN_REGIME_DURATION = 5
GARCH_WINDOW = 22  # Trading days for rolling volatility
TE_WINDOW = 22  # Transfer entropy rolling window
REGIME_LABELS = ["low_volatility", "normal", "elevated", "high_volatility"]


# ─── Data Loading ─────────────────────────────────────────────────


def load_sentiment(path):
    """Load daily_sentiment.csv and prepare for pipeline."""
    df = pd.read_csv(path, parse_dates=["date"], index_col="date")
    df = df.sort_index()

    # Drop the bogus 1969 row
    df = df[df.index >= "2005-01-01"]

    # Create compound score from cross_asset_mean
    df["compound"] = df["cross_asset_mean"].fillna(0)

    # Positive: mean of all asset ensemble means > 0
    asset_cols = [
        c
        for c in df.columns
        if c.endswith("_ensemble_mean") and c != "cross_asset_ensemble_mean"
    ]
    pos_vals = df[asset_cols].clip(lower=0)
    neg_vals = df[asset_cols].clip(upper=0)
    df["positive"] = pos_vals.mean(axis=1).fillna(0)
    df["negative"] = neg_vals.mean(axis=1).fillna(0)
    df["neutral"] = 1 - df["positive"].abs() - df["negative"].abs()
    df["neutral"] = df["neutral"].clip(lower=0)
    df["document_count"] = df.get("total_count", 1).fillna(1).astype(int)

    print(
        f"Sentiment: {len(df)} days, {df.index.min().date()} → {df.index.max().date()}"
    )
    return df


def load_vix(path):
    """Load VIX daily data."""
    df = pd.read_csv(path, parse_dates=["date"], index_col="date")
    df = df.sort_index()
    df.columns = [c.lower() for c in df.columns]
    print(f"VIX: {len(df)} days, {df.index.min().date()} → {df.index.max().date()}")
    return df


def load_ciss(path):
    """Load ECB CISS data."""
    df = pd.read_csv(path)
    # Column names may vary
    date_col = [c for c in df.columns if "DATE" in c.upper()][0]
    val_col = [c for c in df.columns if "CISS" in c.upper() or "IDX" in c.upper()][0]
    df["date"] = pd.to_datetime(df[date_col], errors="coerce")
    df["ciss"] = pd.to_numeric(df[val_col], errors="coerce")
    df = df.dropna(subset=["date", "ciss"]).set_index("date").sort_index()
    df = df[["ciss"]]
    print(f"CISS: {len(df)} days, {df.index.min().date()} → {df.index.max().date()}")
    return df


def load_market(path):
    """Load SPY market data and compute returns."""
    df = pd.read_csv(path, parse_dates=["Date"], index_col="Date")
    df = df.sort_index()
    df.columns = [c.lower() for c in df.columns]

    if "adj close" in df.columns:
        df["returns"] = df["adj close"].pct_change()
    elif "close" in df.columns:
        df["returns"] = df["close"].pct_change()
    else:
        raise ValueError(f"No close/adj close in market data: {df.columns.tolist()}")

    df = df.dropna(subset=["returns"])
    print(
        f"Market (SPY): {len(df)} days, {df.index.min().date()} → {df.index.max().date()}"
    )
    return df


# ─── Feature Engineering ──────────────────────────────────────────


def engineer_features(sentiment, market, vix, ciss):
    """
    Build feature matrix for regime detection.

    Features:
    - compound, positive, negative (sentiment)
    - returns, realized_vol (market)
    - vix, vix_change (VIX)
    - ciss, ciss_change (ECB CISS)
    - transfer_entropy_proxy (rolling correlation sentiment↔VIX)
    - sentiment_momentum (5d rolling change)
    - sentiment_acceleration (momentum change)
    - cross_asset_std (from daily_sentiment.csv)
    """
    # Start with sentiment
    features = sentiment[["compound", "positive", "negative"]].copy()

    # Add cross-asset std if available
    if "cross_asset_std" in sentiment.columns:
        features["cross_asset_std"] = sentiment["cross_asset_std"]

    # Add per-asset ensemble means
    for col in sentiment.columns:
        if col.endswith("_ensemble_mean") and col != "cross_asset_ensemble_mean":
            asset = col.replace("_ensemble_mean", "")
            features[f"sent_{asset}"] = sentiment[col]

    # Intersect with market trading dates
    common_dates = features.index.intersection(market.index)
    print(f"Common trading dates: {len(common_dates)}")

    if len(common_dates) < 100:
        print("WARNING: Very few overlapping dates, using ffill alignment")
        # Reindex sentiment to market dates with forward fill
        features = features.reindex(market.index, method="ffill")
        common_dates = features.index

    features = features.loc[common_dates].copy()

    # Market features
    features["returns"] = market.loc[common_dates, "returns"]
    features["realized_vol"] = features["returns"].rolling(
        GARCH_WINDOW
    ).std() * np.sqrt(252)

    # VIX features
    if vix is not None:
        vix_aligned = vix["close"].reindex(common_dates, method="ffill")
        features["vix"] = vix_aligned
        features["vix_change"] = vix_aligned.pct_change()

    # CISS features
    if ciss is not None:
        ciss_aligned = ciss["ciss"].reindex(common_dates, method="ffill")
        features["ciss"] = ciss_aligned
        features["ciss_change"] = ciss_aligned.diff()

    # Transfer entropy proxy: rolling absolute correlation between compound and VIX
    if "vix" in features.columns:
        features["te_proxy"] = (
            features["compound"]
            .rolling(TE_WINDOW)
            .corr(features["vix"])
            .abs()
            .fillna(0.5)
        )

    # Sentiment momentum (5-day)
    features["sent_momentum"] = features["compound"].diff(5)
    features["sent_acceleration"] = features["sent_momentum"].diff(5)

    # Sentiment dispersion across assets
    asset_sentiment_cols = [c for c in features.columns if c.startswith("sent_")]
    if len(asset_sentiment_cols) >= 2:
        features["sent_dispersion"] = features[asset_sentiment_cols].std(axis=1)
        features["max_divergence"] = features[asset_sentiment_cols].max(
            axis=1
        ) - features[asset_sentiment_cols].min(axis=1)

    # Forward-fill then zero-fill remaining NaNs
    features = features.ffill().fillna(0)

    print(f"Feature matrix: {features.shape[0]} days × {features.shape[1]} features")
    print(f"Features: {features.columns.tolist()}")
    return features


# ─── GARCH(1,1) Volatility ────────────────────────────────────────


def fit_garch(features):
    """
    Fit GARCH(1,1) model to market returns.

    Returns conditional volatility series and model parameters.
    """
    try:
        from arch import arch_model

        returns = features["returns"].dropna() * 100  # Scale for numerical stability
        model = arch_model(returns, vol="Garch", p=1, q=1, dist="t")
        res = model.fit(disp="off")

        cond_vol = res.conditional_volatility / 100  # Scale back
        cond_vol = cond_vol.reindex(features.index, method="ffill")

        params = {
            "omega": float(res.params.get("omega", 0)),
            "alpha": float(res.params.get("alpha[1]", 0)),
            "beta": float(res.params.get("beta[1]", 0)),
            "nu": float(res.params.get("nu", 0)),
            "log_likelihood": float(res.loglikelihood),
            "aic": float(res.aic),
            "bic": float(res.bic),
        }

        persistence = params["alpha"] + params["beta"]
        print(
            f"GARCH(1,1) fitted: α={params['alpha']:.4f}, β={params['beta']:.4f}, persistence={persistence:.4f}"
        )
        print(
            f"  Log-likelihood: {params['log_likelihood']:.2f}, AIC: {params['aic']:.2f}"
        )

        features["garch_vol"] = cond_vol
        features["long_run_vol"] = (
            np.sqrt(params["omega"] / (1 - persistence)) / 100
            if persistence < 1
            else cond_vol.median()
        )

        return params

    except ImportError:
        print("WARNING: arch package not available, using realized volatility proxy")
        features["garch_vol"] = features["realized_vol"]
        features["long_run_vol"] = features["realized_vol"].expanding().mean()
        return {"note": "arch not available, used realized vol proxy"}
    except Exception as e:
        print(f"WARNING: GARCH fitting failed: {e}")
        features["garch_vol"] = features["realized_vol"]
        features["long_run_vol"] = features["realized_vol"].expanding().mean()
        return {"error": str(e), "note": "fell back to realized vol"}


# ─── Statistical Jump Model ───────────────────────────────────────


def fit_jump_model(features):
    """
    Fit Statistical Jump Model for regime classification.

    Uses dynamic programming to find optimal regime segmentation
    that minimizes within-regime variance + jump penalty.
    """
    # Select feature columns for regime detection
    exclude_cols = {"returns", "document_count"}
    feature_cols = [c for c in features.columns if c not in exclude_cols]

    X = features[feature_cols].values.copy()

    # Standardize
    X_mean = np.nanmean(X, axis=0)
    X_std = np.nanstd(X, axis=0)
    X_std[X_std == 0] = 1
    X_norm = (X - X_mean) / X_std
    X_norm = np.nan_to_num(X_norm, nan=0)

    n = len(X_norm)
    k = N_REGIMES
    print(f"Jump Model: {n} observations, {X_norm.shape[1]} features, {k} regimes")

    # Step 1: K-means initialization for regime centroids
    from sklearn.cluster import KMeans

    kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
    initial_labels = kmeans.fit_predict(X_norm)
    centroids = kmeans.cluster_centers_

    # Step 2: Dynamic programming with jump penalty
    # Cost of assigning observation i to regime r
    def cost(i, r):
        diff = X_norm[i] - centroids[r]
        return np.sum(diff**2)

    # Forward pass: Viterbi-like dynamic programming
    dp = np.full((n, k), np.inf)
    backtrack = np.zeros((n, k), dtype=int)

    # Initialize first observation
    for r in range(k):
        dp[0, r] = cost(0, r)

    # Fill DP table
    for t in range(1, n):
        for r in range(k):
            c = cost(t, r)
            for r_prev in range(k):
                penalty = 0 if r == r_prev else JUMP_PENALTY
                total = dp[t - 1, r_prev] + c + penalty
                if total < dp[t, r]:
                    dp[t, r] = total
                    backtrack[t, r] = r_prev

    # Backtrack to find optimal path
    regimes = np.zeros(n, dtype=int)
    regimes[-1] = np.argmin(dp[-1])
    for t in range(n - 2, -1, -1):
        regimes[t] = backtrack[t + 1, regimes[t + 1]]

    # Step 3: Re-estimate centroids and iterate (2 more passes)
    for iteration in range(2):
        # Update centroids
        for r in range(k):
            mask = regimes == r
            if mask.sum() > 0:
                centroids[r] = X_norm[mask].mean(axis=0)

        # Re-run DP
        dp = np.full((n, k), np.inf)
        backtrack = np.zeros((n, k), dtype=int)
        for r in range(k):
            dp[0, r] = cost(0, r)
        for t in range(1, n):
            for r in range(k):
                c = cost(t, r)
                for r_prev in range(k):
                    penalty = 0 if r == r_prev else JUMP_PENALTY
                    total = dp[t - 1, r_prev] + c + penalty
                    if total < dp[t, r]:
                        dp[t, r] = total
                        backtrack[t, r] = r_prev
        regimes[-1] = np.argmin(dp[-1])
        for t in range(n - 2, -1, -1):
            regimes[t] = backtrack[t + 1, regimes[t + 1]]

    # Step 4: Order regimes by mean VIX (if available) or volatility
    regime_vix_means = {}
    for r in range(k):
        mask = regimes == r
        if mask.sum() > 0:
            if "vix" in features.columns:
                regime_vix_means[r] = features["vix"].values[mask].mean()
            elif "garch_vol" in features.columns:
                regime_vix_means[r] = features["garch_vol"].values[mask].mean()
            else:
                regime_vix_means[r] = features["realized_vol"].values[mask].mean()

    # Sort regimes by VIX/vol level (lowest = low_volatility, highest = high_volatility)
    sorted_regimes = sorted(regime_vix_means.keys(), key=lambda r: regime_vix_means[r])
    regime_map = {old: new for new, old in enumerate(sorted_regimes)}
    regimes = np.array([regime_map[r] for r in regimes])

    # Map to labels
    regime_labels = [REGIME_LABELS[r % len(REGIME_LABELS)] for r in regimes]

    # Statistics
    regime_series = pd.Series(regime_labels, index=features.index, name="regime")
    transitions = (regime_series != regime_series.shift(1)).sum() - 1
    avg_duration = (
        len(regime_series) / (transitions + 1)
        if transitions >= 0
        else len(regime_series)
    )

    print(f"\nRegime distribution:")
    for label, count in regime_series.value_counts().items():
        pct = count / len(regime_series) * 100
        print(f"  {label}: {count} days ({pct:.1f}%)")
    print(f"Transitions: {transitions}, avg regime duration: {avg_duration:.1f} days")

    return regime_series, {
        "n_regimes": k,
        "jump_penalty": JUMP_PENALTY,
        "n_transitions": int(transitions),
        "avg_regime_duration": float(avg_duration),
        "regime_distribution": {
            label: float(count / len(regime_series))
            for label, count in regime_series.value_counts().items()
        },
        "regime_vix_means": {
            REGIME_LABELS[regime_map[r]]: float(v) for r, v in regime_vix_means.items()
        },
    }


# ─── Event Validation ─────────────────────────────────────────────


def validate_against_events(regime_series):
    """Check regime labels against known market events."""
    events = {
        "2008-09-15": ("Lehman Brothers", "high_volatility"),
        "2008-10-15": ("GFC peak", "high_volatility"),
        "2020-03-16": ("COVID crash", "high_volatility"),
        "2020-03-23": ("COVID bottom", "high_volatility"),
        "2021-01-27": ("GameStop squeeze", "elevated"),
        "2022-06-13": ("Bear market 2022", "elevated"),
        "2017-01-03": ("Bull market rally", "low_volatility"),
        "2019-07-15": ("Pre-COVID calm", "low_volatility"),
    }

    print("\n=== Event Validation ===")
    matches = 0
    total = 0
    for date_str, (event_name, expected) in events.items():
        date = pd.Timestamp(date_str)
        # Find nearest date in series
        if date in regime_series.index:
            actual = regime_series.loc[date]
        else:
            nearest_idx = regime_series.index.get_indexer([date], method="nearest")[0]
            if nearest_idx >= 0:
                actual = regime_series.iloc[nearest_idx]
                date = regime_series.index[nearest_idx]
            else:
                print(f"  {event_name} ({date_str}): NOT IN RANGE")
                continue

        match = "✓" if actual == expected else "✗"
        if actual == expected:
            matches += 1
        total += 1
        print(
            f"  {match} {event_name} ({date.date()}): expected={expected}, got={actual}"
        )

    if total > 0:
        print(f"\nEvent accuracy: {matches}/{total} ({matches / total * 100:.0f}%)")


# ─── Main ─────────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Run regime detection pipeline")
    parser.add_argument(
        "--sentiment", required=True, help="Path to daily_sentiment.csv"
    )
    parser.add_argument("--vix", required=True, help="Path to VIX daily CSV")
    parser.add_argument("--ciss", required=True, help="Path to ECB CISS CSV")
    parser.add_argument("--market", required=True, help="Path to SPY ETF CSV")
    parser.add_argument(
        "--output-dir", required=True, help="Output directory for results"
    )
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    start_time = time.time()

    print("=" * 60)
    print("REGIME DETECTION PIPELINE")
    print("=" * 60)

    # Stage 0: Load data
    print("\n--- Stage 0: Loading Data ---")
    sentiment = load_sentiment(args.sentiment)
    vix = load_vix(args.vix)
    ciss = load_ciss(args.ciss)
    market = load_market(args.market)

    # Stage 1: Feature engineering (alignment is implicit — data is already daily)
    print("\n--- Stage 1: Feature Engineering ---")
    features = engineer_features(sentiment, market, vix, ciss)

    # Stage 2: GARCH(1,1) volatility
    print("\n--- Stage 2: GARCH(1,1) Volatility ---")
    garch_params = fit_garch(features)

    # Stage 3: Jump model regime classification
    print("\n--- Stage 3: Statistical Jump Model ---")
    regime_series, jump_stats = fit_jump_model(features)

    # Stage 4: Validate against known events
    validate_against_events(regime_series)

    # Stage 5: Export results
    print("\n--- Stage 5: Exporting Results ---")

    # Regime labels
    regime_path = os.path.join(args.output_dir, "regime_labels.csv")
    regime_df = regime_series.to_frame()
    regime_df["regime_id"] = regime_series.map(
        {"low_volatility": 0, "normal": 1, "elevated": 2, "high_volatility": 3}
    )
    regime_df.to_csv(regime_path)
    print(f"  Saved regime labels: {regime_path}")

    # Feature matrix
    features_path = os.path.join(args.output_dir, "feature_matrix.csv")
    features["regime"] = regime_series
    features.to_csv(features_path)
    print(f"  Saved feature matrix: {features_path}")

    # Transitions
    transitions_mask = regime_series != regime_series.shift(1)
    transitions_df = regime_series[transitions_mask].to_frame()
    transitions_df["from_regime"] = regime_series.shift(1)[transitions_mask]
    transitions_df["to_regime"] = regime_series[transitions_mask]
    transitions_df = transitions_df.iloc[1:]  # Drop first (no "from")
    transitions_path = os.path.join(args.output_dir, "regime_transitions.csv")
    transitions_df.to_csv(transitions_path)
    print(
        f"  Saved transitions: {transitions_path} ({len(transitions_df)} transitions)"
    )

    # Summary JSON
    elapsed = time.time() - start_time
    summary = {
        "pipeline_version": "2.0",
        "run_timestamp": datetime.now().isoformat(),
        "processing_time_seconds": round(elapsed, 2),
        "data": {
            "sentiment_days": len(sentiment),
            "feature_matrix_days": len(features),
            "date_range": [
                str(features.index.min().date()),
                str(features.index.max().date()),
            ],
            "n_features": len(features.columns) - 1,  # Exclude regime column
        },
        "garch": garch_params,
        "jump_model": jump_stats,
        "output_files": {
            "regime_labels": regime_path,
            "feature_matrix": features_path,
            "transitions": transitions_path,
        },
    }
    summary_path = os.path.join(args.output_dir, "pipeline_summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"  Saved summary: {summary_path}")

    print(f"\n{'=' * 60}")
    print(f"PIPELINE COMPLETE in {elapsed:.1f}s")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
