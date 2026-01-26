"""Alert management endpoints."""

from datetime import datetime, timezone
from typing import Literal
from uuid import UUID, uuid4

from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel, Field

router = APIRouter()

AlertType = Literal["regime_change", "divergence", "sentiment_spike", "custom"]
Severity = Literal["info", "warning", "critical"]


class AlertConfig(BaseModel):
    """Alert configuration schema."""

    alert_type: AlertType
    conditions: dict = Field(
        ...,
        description="Conditions that trigger the alert",
        examples=[{"regime_change_to": "risk_off", "confidence_min": 0.7}],
    )
    enabled: bool = True


class AlertConfigResponse(AlertConfig):
    """Alert configuration response with ID."""

    id: UUID
    created_at: datetime


class AlertHistoryItem(BaseModel):
    """Historical alert record."""

    id: UUID
    config_id: UUID
    alert_type: AlertType
    severity: Severity
    message: str
    data: dict
    triggered_at: datetime
    acknowledged: bool = False


# In-memory storage for demo (will be replaced with database)
_alert_configs: dict[UUID, AlertConfigResponse] = {}


@router.post("/subscribe", response_model=AlertConfigResponse)
async def subscribe_to_alerts(config: AlertConfig) -> AlertConfigResponse:
    """
    Subscribe to alerts based on specified conditions.
    
    Alert Types:
        - regime_change: Triggered when market regime changes
        - divergence: Triggered when cross-asset divergence exceeds threshold
        - sentiment_spike: Triggered on sudden sentiment shifts
        - custom: Custom conditions
    
    Example conditions:
        - {"regime_change_to": "risk_off"}
        - {"divergence_threshold": 0.5}
        - {"sentiment_drop_threshold": -0.3, "asset_class": "crypto"}
    """
    alert_id = uuid4()
    response = AlertConfigResponse(
        id=alert_id,
        alert_type=config.alert_type,
        conditions=config.conditions,
        enabled=config.enabled,
        created_at=datetime.now(timezone.utc),
    )
    
    _alert_configs[alert_id] = response
    return response


@router.get("/subscriptions", response_model=list[AlertConfigResponse])
async def list_subscriptions() -> list[AlertConfigResponse]:
    """List all active alert subscriptions."""
    return list(_alert_configs.values())


@router.delete("/subscriptions/{alert_id}")
async def delete_subscription(alert_id: UUID) -> dict[str, str]:
    """Delete an alert subscription."""
    if alert_id not in _alert_configs:
        raise HTTPException(status_code=404, detail="Alert subscription not found")
    
    del _alert_configs[alert_id]
    return {"status": "deleted", "id": str(alert_id)}


@router.get("/history", response_model=list[AlertHistoryItem])
async def get_alert_history(
    alert_type: AlertType | None = Query(default=None, description="Filter by alert type"),
    severity: Severity | None = Query(default=None, description="Filter by severity"),
    limit: int = Query(default=50, le=200, description="Max alerts to return"),
    unacknowledged_only: bool = Query(default=False, description="Only show unacknowledged"),
) -> list[AlertHistoryItem]:
    """
    Get history of triggered alerts.
    
    Supports filtering by type, severity, and acknowledgment status.
    """
    # TODO: Implement real alert history retrieval from database
    
    # Return example alert for API structure demonstration
    return [
        AlertHistoryItem(
            id=uuid4(),
            config_id=uuid4(),
            alert_type="regime_change",
            severity="warning",
            message="Regime transition detected: risk_on → transition",
            data={
                "from_regime": "risk_on",
                "to_regime": "transition",
                "confidence": 0.68,
                "trigger_features": {
                    "crypto_sentiment_drop": -0.25,
                },
            },
            triggered_at=datetime.now(timezone.utc),
            acknowledged=False,
        ),
    ]


@router.post("/history/{alert_id}/acknowledge")
async def acknowledge_alert(alert_id: UUID) -> dict[str, str]:
    """Mark an alert as acknowledged."""
    # TODO: Implement real acknowledgment in database
    
    return {"status": "acknowledged", "id": str(alert_id)}
