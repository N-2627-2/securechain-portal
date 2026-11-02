from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()


class AlertPayload(BaseModel):
    alert_id: str
    severity: str
    src_ip: str
    sensor_id: str
    rule_name: str
    timestamp: datetime


class QuarantinePayload(BaseModel):
    node_id: str
    reason: str
    approved_by: str
    ttl_minutes: Optional[int] = 60


@router.post("/alerts", status_code=status.HTTP_201_CREATED, tags=["SOC Integration"])
async def receive_alert(payload: AlertPayload):
    """Receive and log security alerts from the SOC alert shipper."""
    return {
        "status": "received",
        "alert_id": payload.alert_id,
        "message": f"Alert {payload.alert_id} queued for n8n triage.",
    }


@router.post("/quarantine", status_code=status.HTTP_202_ACCEPTED, tags=["Quarantine"])
async def trigger_quarantine(payload: QuarantinePayload):
    """Trigger node quarantine after human-in-the-loop approval."""

    if payload.node_id in ["10.20.10.1", "10.20.40.10"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": "PROTECTED_NODE", "message": "Node is on the critical allowlist."},
        )
    return {
        "status": "active",
        "quarantine_id": f"qtn-{payload.node_id}",
        "node_id": payload.node_id,
        "approved_by": payload.approved_by,
    }