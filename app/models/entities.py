from __future__ import annotations

import enum
from datetime import datetime, date

from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Enum, ForeignKey, Numeric
from sqlalchemy.orm import relationship, Mapped

from ..core.database import Base


class VendorStatus(enum.Enum):
    Active = "Active"
    Inactive = "Inactive"


class ServiceStatus(enum.Enum):
    Active = "Active"
    Expired = "Expired"
    Payment_Pending = "Payment Pending"
    Completed = "Completed"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    email: Mapped[str] = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = Column(String(255), nullable=False)
    is_active: Mapped[bool] = Column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class Vendor(Base):
    __tablename__ = "vendors"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    name: Mapped[str] = Column(String(255), nullable=False, index=True)
    contact_person: Mapped[str] = Column(String(255), nullable=False)
    email: Mapped[str] = Column(String(255), nullable=False)
    phone: Mapped[str] = Column(String(50), nullable=False)
    status: Mapped[VendorStatus] = Column(Enum(VendorStatus, native_enum=False), default=VendorStatus.Active, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    services = relationship("ServiceContract", back_populates="vendor", cascade="all, delete-orphan")


class ServiceContract(Base):
    __tablename__ = "services"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    vendor_id: Mapped[int] = Column(Integer, ForeignKey("vendors.id", ondelete="CASCADE"), nullable=False, index=True)
    service_name: Mapped[str] = Column(String(255), nullable=False, index=True)
    start_date: Mapped[date] = Column(Date, nullable=False)
    expiry_date: Mapped[date] = Column(Date, nullable=False)
    payment_due_date: Mapped[date] = Column(Date, nullable=False)
    amount: Mapped[float] = Column(Numeric(12, 2), nullable=False)
    status: Mapped[ServiceStatus] = Column(Enum(ServiceStatus, native_enum=False), default=ServiceStatus.Active, nullable=False)
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    vendor = relationship("Vendor", back_populates="services")


