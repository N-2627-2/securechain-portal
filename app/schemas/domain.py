from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: Optional[str] = None
    role: Optional[str] = None
    tenant_id: Optional[str] = None


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "Consumer"


class UserCreate(UserBase):
    password: str
    tenant_id: str


class UserResponse(UserBase):
    id: str
    tenant_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ShipmentBase(BaseModel):
    tracking_number: str
    destination: str
    status: str = "IN_TRANSIT"
    eta: datetime
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ShipmentCreate(ShipmentBase):
    tenant_id: str


class ShipmentUpdateETA(BaseModel):
    eta: datetime
    reason: Optional[str] = None


class ShipmentResponse(ShipmentBase):
    id: str
    tenant_id: str
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)