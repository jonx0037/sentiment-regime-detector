"""GARCH volatility modeling endpoints."""

import json
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException

router = APIRouter()


def load_latest_garch_results() -> Optional[dict]:
    """Load the most recent GARCH results file."""
    # Resolve project root: try multiple strategies to find results dir
    # Strategy 1: Walk up from this source file
    source_dir = Path(__file__).resolve().parent
    for _ in range(6):
        source_dir = source_dir.parent
        candidate = source_dir / "results"
        if candidate.exists() and list(candidate.glob("garch_midas_results_*.json")):
            results_dir = candidate
            break
    else:
        # Strategy 2: Check common working directories
        for base in [Path.cwd(), Path("/app"), Path.home()]:
            candidate = base / "results"
            if candidate.exists():
                results_dir = candidate
                break
        else:
            return None

    # Find all GARCH results files
    garch_files = sorted(results_dir.glob("garch_midas_results_*.json"), reverse=True)
    if not garch_files:
        return None

    # Load the most recent file
    with open(garch_files[0]) as f:
        return json.load(f)


@router.get("/results")
async def get_garch_results() -> dict:
    """
    Get latest GARCH-MIDAS volatility model results.

    Returns:
        - Model parameters (μ, ω, α, β)
        - Information criteria (AIC, BIC)
        - Conditional volatility forecast
        - MIDAS component (if available)
    """
    results = load_latest_garch_results()
    if not results:
        raise HTTPException(status_code=404, detail="No GARCH results available")

    return results


@router.get("/volatility/forecast")
async def get_volatility_forecast(
    horizon: int = 30,
) -> dict:
    """
    Get volatility forecast for the next N days.

    Args:
        horizon: Number of days to forecast (default: 30)

    Returns:
        - Forecasted volatility values
        - Confidence intervals
        - Mean forecast
    """
    results = load_latest_garch_results()
    if not results:
        raise HTTPException(status_code=404, detail="No GARCH results available")

    baseline = results.get("baseline_garch", {})
    if "conditional_volatility" not in baseline:
        raise HTTPException(status_code=404, detail="No volatility forecast available")

    # Get the most recent volatility values (last 30 or horizon days)
    vol_series = baseline["conditional_volatility"]
    forecast_values = vol_series[-horizon:] if len(vol_series) >= horizon else vol_series

    # Calculate statistics
    mean_vol = sum(forecast_values) / len(forecast_values) if forecast_values else 0
    max_vol = max(forecast_values) if forecast_values else 0
    min_vol = min(forecast_values) if forecast_values else 0

    return {
        "horizon": horizon,
        "forecast": forecast_values,
        "statistics": {
            "mean": mean_vol,
            "max": max_vol,
            "min": min_vol,
        },
        "model": {
            "params": baseline.get("params", {}),
            "aic": baseline.get("aic"),
            "bic": baseline.get("bic"),
        },
    }


@router.get("/parameters")
async def get_garch_parameters() -> dict:
    """
    Get GARCH model parameters and diagnostics.

    Returns:
        - Model parameters (mean, omega, alpha, beta)
        - Volatility persistence (α + β)
        - Model fit statistics
    """
    results = load_latest_garch_results()
    if not results:
        raise HTTPException(status_code=404, detail="No GARCH results available")

    baseline = results.get("baseline_garch", {})
    params = baseline.get("params", {})

    # Calculate volatility persistence
    alpha = params.get("alpha[1]", 0)
    beta = params.get("beta[1]", 0)
    persistence = alpha + beta

    return {
        "parameters": params,
        "persistence": persistence,
        "aic": baseline.get("aic"),
        "bic": baseline.get("bic"),
        "loglikelihood": baseline.get("loglikelihood"),
        "interpretation": {
            "persistence": "high"
            if persistence > 0.9
            else "moderate"
            if persistence > 0.7
            else "low",
            "shock_impact": "high" if alpha > 0.2 else "moderate" if alpha > 0.1 else "low",
            "memory": "high" if beta > 0.85 else "moderate" if beta > 0.7 else "low",
        },
    }
