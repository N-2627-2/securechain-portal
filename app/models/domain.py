from datetime import datetime, timezone
import uuid
from sqlalchemy import String, DateTime, ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base


class Tenant(Base):
    __tablename__ = "tenants"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    users = relationship("User", back_populates="tenant", cascade="all, delete-orphan")
    shipments = relationship("Shipment", back_populates="tenant", cascade="all, delete-orphan")


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="Consumer")
    tenant_id: Mapped[str] = mapped_column(String, ForeignKey("tenants.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    tenant = relationship("Tenant", back_populates="users")


class Shipment(Base):
    __tablename__ = "shipments"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    tracking_number: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="IN_TRANSIT")
    destination: Mapped[str] = mapped_column(String(255), nullable=False)
    eta: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    tenant_id: Mapped[str] = mapped_column(String, ForeignKey("tenants.id"), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    tenant = relationship("Tenant", back_populates="shipments")