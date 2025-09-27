from __future__ import annotations

from datetime import date, timedelta
from typing import List, Optional

from ..core.config import settings
from ..domain.repositories import VendorRepository, ServiceContractRepository
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


class VendorService:
    def __init__(self, vendor_repo: VendorRepository) -> None:
        self.vendor_repo = vendor_repo

    def create_vendor(self, data: VendorCreate) -> VendorOut:
        return self.vendor_repo.create(data)

    def list_vendors(self, limit: int, offset: int) -> List[VendorOut]:
        return self.vendor_repo.list(limit, offset)

    def count_vendors(self) -> int:
        return self.vendor_repo.count()

    def get_vendor(self, vendor_id: int) -> Optional[VendorOut]:
        return self.vendor_repo.get(vendor_id)

    def update_vendor(self, vendor_id: int, data: VendorUpdate) -> Optional[VendorOut]:
        return self.vendor_repo.update(vendor_id, data)

    def delete_vendor(self, vendor_id: int) -> bool:
        return self.vendor_repo.delete(vendor_id)

    def list_vendors_with_active_services(self, limit: int, offset: int) -> List[VendorWithActiveServices]:
        # Repo returns DTOs with services; we enrich with flags here for consistency
        vendors = self.vendor_repo.list_with_active_services(limit, offset)
        enriched: List[VendorWithActiveServices] = []
        for v in vendors:
            services: List[ServiceOut] = []
            for s in v.services:
                services.append(
                    ServiceOut(
                        id=s.id,
                        vendor_id=s.vendor_id,
                        service_name=s.service_name,
                        start_date=s.start_date,
                        expiry_date=s.expiry_date,
                        payment_due_date=s.payment_due_date,
                        amount=s.amount,
                        status=s.status,
                        created_at=s.created_at,
                        expiry_flag=expiry_flag(s.expiry_date),
                        payment_flag=payment_flag(s.payment_due_date),
                    )
                )
            enriched.append(
                VendorWithActiveServices(
                    id=v.id,
                    name=v.name,
                    contact_person=v.contact_person,
                    email=v.email,
                    phone=v.phone,
                    status=v.status,
                    created_at=v.created_at,
                    services=services,
                )
            )
        return enriched


class ServiceContractService:
    def __init__(self, service_repo: ServiceContractRepository) -> None:
        self.service_repo = service_repo

    def create_service(self, vendor_id: int, data: ServiceCreate) -> ServiceOut:
        s = self.service_repo.create_for_vendor(vendor_id, data)
        s.expiry_flag = expiry_flag(s.expiry_date)
        s.payment_flag = payment_flag(s.payment_due_date)
        return s

    def list_services_for_vendor(self, vendor_id: int, limit: int, offset: int) -> List[ServiceOut]:
        items = self.service_repo.list_for_vendor(vendor_id, limit, offset)
        for s in items:
            s.expiry_flag = expiry_flag(s.expiry_date)
            s.payment_flag = payment_flag(s.payment_due_date)
        return items

    def update_service(self, service_id: int, data: ServiceUpdate) -> Optional[ServiceOut]:
        s = self.service_repo.update(service_id, data)
        if s:
            s.expiry_flag = expiry_flag(s.expiry_date)
            s.payment_flag = payment_flag(s.payment_due_date)
        return s

    def delete_service(self, service_id: int) -> bool:
        return self.service_repo.delete(service_id)

    def update_service_status(self, service_id: int, status: str) -> Optional[ServiceOut]:
        s = self.service_repo.update(service_id, ServiceUpdate(status=status))
        if s:
            s.expiry_flag = expiry_flag(s.expiry_date)
            s.payment_flag = payment_flag(s.payment_due_date)
        return s

    def services_expiring(self, days: int, limit: int, offset: int) -> List[ServiceOut]:
        cutoff = date.today() + timedelta(days=days)
        items = self.service_repo.list_expiring_before(cutoff, limit, offset)
        for s in items:
            s.expiry_flag = expiry_flag(s.expiry_date)
            s.payment_flag = payment_flag(s.payment_due_date)
        return items

    def services_payment_due(self, days: int, limit: int, offset: int) -> List[ServiceOut]:
        cutoff = date.today() + timedelta(days=days)
        items = self.service_repo.list_payment_due_before(cutoff, limit, offset)
        for s in items:
            s.expiry_flag = expiry_flag(s.expiry_date)
            s.payment_flag = payment_flag(s.payment_due_date)
        return items


