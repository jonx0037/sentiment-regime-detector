"""Tests for regime endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_current_regime(client: AsyncClient) -> None:
    """Test current regime endpoint returns valid regime state."""
    response = await client.get("/api/v1/regime/current")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "timestamp" in data
    assert data["regime"] in ["risk_on", "risk_off", "transition"]
    assert 0 <= data["confidence"] <= 1
    assert "probabilities" in data
    assert "features" in data
    assert "model_version" in data


@pytest.mark.asyncio
async def test_get_regime_transitions(client: AsyncClient) -> None:
    """Test regime transitions endpoint."""
    response = await client.get("/api/v1/regime/transitions?limit=5")
    
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_cross_asset_divergence(client: AsyncClient) -> None:
    """Test divergence analysis endpoint."""
    response = await client.get("/api/v1/regime/divergence")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "divergence_score" in data
    assert "pairs" in data
