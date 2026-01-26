"""Tests for sentiment endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_current_sentiment(client: AsyncClient) -> None:
    """Test current sentiment endpoint returns all asset classes."""
    response = await client.get("/api/v1/sentiment/current")
    
    assert response.status_code == 200
    data = response.json()
    
    assert "timestamp" in data
    assert "asset_classes" in data
    assert len(data["asset_classes"]) == 4  # equity, crypto, forex, commodity
    
    # Check each asset class has required fields
    for asset in data["asset_classes"]:
        assert "asset_class" in asset
        assert "compound_score" in asset
        assert "positive_ratio" in asset
        assert "negative_ratio" in asset
        assert "sample_count" in asset


@pytest.mark.asyncio
async def test_get_sentiment_by_source(client: AsyncClient) -> None:
    """Test sentiment by source endpoint."""
    response = await client.get("/api/v1/sentiment/by-source?asset_class=equity")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["asset_class"] == "equity"
    assert "sources" in data


@pytest.mark.asyncio
async def test_get_sentiment_history_requires_params(client: AsyncClient) -> None:
    """Test sentiment history requires asset_class and start_date."""
    response = await client.get("/api/v1/sentiment/history")
    
    # Should fail without required parameters
    assert response.status_code == 422
