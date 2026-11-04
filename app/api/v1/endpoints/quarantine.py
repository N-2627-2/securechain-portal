from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, UUID4
from typing import Optional, Literal
from datetime import datetime, timezone, timedelta
import uuid
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Quarantine"])

SeverityEnum = Literal["low", "medium", "high", "critical"]
QuarantineStatusEnum = Literal["pending", "active", "released", "failed"]

class QuarantineRequest(BaseModel):
    alert_id: UUID4
    node_id: str
    site_id: str
    reason: str
    severity: SeverityEnum
    approved_by: Optional[str] = None
    expires_in_minutes: int = Field(default=60, ge=1)

class QuarantineStatusResponse(BaseModel):
    quarantine_id: UUID4
    node_id: str
    status: QuarantineStatusEnum
    applied_at: Optional[str] = None
    expires_at: Optional[str] = None
    audit_id: Optional[str] = None

@router.post(
    "/quarantine",
    response_model=QuarantineStatusResponse,
    status_code=status.HTTP_202_ACCEPTED
)
async def quarantine_node(payload: QuarantineRequest):
    # Guardrail: High/Critical severity requires explicit approval
    if payload.severity in ["high", "critical"] and not payload.approved_by:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "code": "APPROVAL_REQUIRED",
                "message": "High or critical severity isolation requires an approved_by identity."
            }
        )

    logger.info(f"Accepted quarantine request for node '{payload.node_id}' under alert '{payload.alert_id}'")

    now = datetime.now(timezone.utc)
    expires = now + timedelta(minutes=payload.expires_in_minutes)

    return QuarantineStatusResponse(
        quarantine_id=uuid.uuid4(),
        node_id=payload.node_id,
        status="active",
        applied_at=now.isoformat(),
        expires_at=expires.isoformat(),
        audit_id=f"audit-{uuid.uuid4().hex[:8]}"
    )