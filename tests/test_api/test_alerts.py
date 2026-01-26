"""Tests for alert endpoints."""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_subscribe_to_alerts(client: AsyncClient) -> None:
    """Test creating an alert subscription."""
    response = await client.post(
        "/api/v1/alerts/subscribe",
        json={
            "alert_type": "regime_change",
            "conditions": {"regime_change_to": "risk_off"},
            "enabled": True,
        },
    )
    
    assert response.status_code == 200
    data = response.json()
    
    assert "id" in data
    assert data["alert_type"] == "regime_change"
    assert data["enabled"] is True


@pytest.mark.asyncio
async def test_list_subscriptions(client: AsyncClient) -> None:
    """Test listing alert subscriptions."""
    # First create a subscription
    await client.post(
        "/api/v1/alerts/subscribe",
        json={
            "alert_type": "divergence",
            "conditions": {"threshold": 0.5},
        },
    )
    
    response = await client.get("/api/v1/alerts/subscriptions")
    
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)


@pytest.mark.asyncio
async def test_get_alert_history(client: AsyncClient) -> None:
    """Test retrieving alert history."""
    response = await client.get("/api/v1/alerts/history")
    
    assert response.status_code == 200
    data = response.json()
    
    assert isinstance(data, list)
