from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional, Literal

from pydantic import BaseModel, EmailStr, Field


# Auth
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=6)


class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# Vendor
VendorStatusLiteral = Literal["Active", "Inactive"]


class VendorBase(BaseModel):
    name: str
    contact_person: str
    email: EmailStr
    phone: str
    status: VendorStatusLiteral = "Active"


class VendorCreate(VendorBase):
    pass


class VendorUpdate(BaseModel):
    name: Optional[str] = None
    contact_person: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    status: Optional[VendorStatusLiteral] = None


class VendorOut(VendorBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Service
ServiceStatusLiteral = Literal["Active", "Expired", "Payment Pending", "Completed"]


class ServiceBase(BaseModel):
    service_name: str
    start_date: date
    expiry_date: date
    payment_due_date: date
    amount: float
    status: ServiceStatusLiteral = "Active"


class ServiceCreate(ServiceBase):
    pass


class ServiceUpdate(BaseModel):
    service_name: Optional[str] = None
    start_date: Optional[date] = None
    expiry_date: Optional[date] = None
    payment_due_date: Optional[date] = None
    amount: Optional[float] = None
    status: Optional[ServiceStatusLiteral] = None


class ServiceStatusUpdate(BaseModel):
    status: ServiceStatusLiteral


class ServiceOut(ServiceBase):
    id: int
    vendor_id: int
    created_at: datetime
    expiry_flag: Optional[str] = None
    payment_flag: Optional[str] = None

    class Config:
        from_attributes = True


class VendorWithActiveServices(VendorOut):
    services: List[ServiceOut] = []


# Pagination
class PaginatedResponse(BaseModel):
    total: int
    limit: int
    offset: int


