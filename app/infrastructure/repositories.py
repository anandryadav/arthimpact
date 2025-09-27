from __future__ import annotations

from datetime import date
from typing import List, Optional

from sqlalchemy.orm import Session

from ..domain.repositories import VendorRepository, ServiceContractRepository
from ..models.entities import Vendor, VendorStatus, ServiceContract, ServiceStatus
from ..schemas.models import (
    VendorCreate,
    VendorUpdate,
    VendorOut,
    VendorWithActiveServices,
    ServiceCreate,
    ServiceUpdate,
    ServiceOut,
)
from ..utils.flags import expiry_flag, payment_flag


def to_vendor_out(v: Vendor) -> VendorOut:
    return VendorOut(
        id=v.id,
        name=v.name,
        contact_person=v.contact_person,
        email=v.email,
        phone=v.phone,
        status=v.status.value,
        created_at=v.created_at,
    )


def to_service_out(s: ServiceContract) -> ServiceOut:
    return ServiceOut(
        id=s.id,
        vendor_id=s.vendor_id,
        service_name=s.service_name,
        start_date=s.start_date,
        expiry_date=s.expiry_date,
        payment_due_date=s.payment_due_date,
        amount=float(s.amount),
        status=s.status.value,
        created_at=s.created_at,
        expiry_flag=expiry_flag(s.expiry_date),
        payment_flag=payment_flag(s.payment_due_date),
    )


class SqlAlchemyVendorRepository(VendorRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, data: VendorCreate) -> VendorOut:
        vendor = Vendor(
            name=data.name,
            contact_person=data.contact_person,
            email=data.email,
            phone=data.phone,
            status=VendorStatus(data.status),
        )
        self.db.add(vendor)
        self.db.commit()
        self.db.refresh(vendor)
        return to_vendor_out(vendor)

    def get(self, vendor_id: int) -> Optional[VendorOut]:
        v = self.db.query(Vendor).filter(Vendor.id == vendor_id).first()
        return to_vendor_out(v) if v else None

    def list(self, limit: int, offset: int) -> List[VendorOut]:
        vendors = (
            self.db.query(Vendor).order_by(Vendor.created_at.desc()).limit(limit).offset(offset).all()
        )
        return [to_vendor_out(v) for v in vendors]

    def count(self) -> int:
        return self.db.query(Vendor).count()

    def update(self, vendor_id: int, data: VendorUpdate) -> Optional[VendorOut]:
        v = self.db.query(Vendor).filter(Vendor.id == vendor_id).first()
        if not v:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            if field == "status" and value is not None:
                setattr(v, field, VendorStatus(value))
            elif value is not None:
                setattr(v, field, value)
        self.db.add(v)
        self.db.commit()
        self.db.refresh(v)
        return to_vendor_out(v)

    def delete(self, vendor_id: int) -> bool:
        v = self.db.query(Vendor).filter(Vendor.id == vendor_id).first()
        if not v:
            return False
        self.db.delete(v)
        self.db.commit()
        return True

    def list_with_active_services(self, limit: int, offset: int) -> List[VendorWithActiveServices]:
        vendors = (
            self.db.query(Vendor)
            .filter(Vendor.status == VendorStatus.Active)
            .order_by(Vendor.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        result: List[VendorWithActiveServices] = []
        for v in vendors:
            active_services = [s for s in v.services if s.status == ServiceStatus.Active]
            result.append(
                VendorWithActiveServices(
                    id=v.id,
                    name=v.name,
                    contact_person=v.contact_person,
                    email=v.email,
                    phone=v.phone,
                    status=v.status.value,
                    created_at=v.created_at,
                    services=[to_service_out(s) for s in active_services],
                )
            )
        return result


class SqlAlchemyServiceContractRepository(ServiceContractRepository):
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_for_vendor(self, vendor_id: int, data: ServiceCreate) -> ServiceOut:
        s = ServiceContract(
            vendor_id=vendor_id,
            service_name=data.service_name,
            start_date=data.start_date,
            expiry_date=data.expiry_date,
            payment_due_date=data.payment_due_date,
            amount=data.amount,
            status=ServiceStatus(data.status),
        )
        self.db.add(s)
        self.db.commit()
        self.db.refresh(s)
        return to_service_out(s)

    def get(self, service_id: int) -> Optional[ServiceOut]:
        s = self.db.query(ServiceContract).filter(ServiceContract.id == service_id).first()
        return to_service_out(s) if s else None

    def list_for_vendor(self, vendor_id: int, limit: int, offset: int) -> List[ServiceOut]:
        items = (
            self.db.query(ServiceContract)
            .filter(ServiceContract.vendor_id == vendor_id)
            .order_by(ServiceContract.created_at.desc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        return [to_service_out(s) for s in items]

    def update(self, service_id: int, data: ServiceUpdate) -> Optional[ServiceOut]:
        s = self.db.query(ServiceContract).filter(ServiceContract.id == service_id).first()
        if not s:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            if field == "status" and value is not None:
                setattr(s, field, ServiceStatus(value))
            elif value is not None:
                setattr(s, field, value)
        self.db.add(s)
        self.db.commit()
        self.db.refresh(s)
        return to_service_out(s)

    def delete(self, service_id: int) -> bool:
        s = self.db.query(ServiceContract).filter(ServiceContract.id == service_id).first()
        if not s:
            return False
        self.db.delete(s)
        self.db.commit()
        return True

    def list_expiring_before(self, cutoff: date, limit: int, offset: int) -> List[ServiceOut]:
        items = (
            self.db.query(ServiceContract)
            .filter(ServiceContract.expiry_date <= cutoff)
            .order_by(ServiceContract.expiry_date.asc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        return [to_service_out(s) for s in items]

    def list_payment_due_before(self, cutoff: date, limit: int, offset: int) -> List[ServiceOut]:
        items = (
            self.db.query(ServiceContract)
            .filter(ServiceContract.payment_due_date <= cutoff)
            .order_by(ServiceContract.payment_due_date.asc())
            .limit(limit)
            .offset(offset)
            .all()
        )
        return [to_service_out(s) for s in items]


