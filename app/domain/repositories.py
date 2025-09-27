from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional, Tuple

from ..schemas import VendorCreate, VendorUpdate, VendorOut, VendorWithActiveServices, ServiceCreate, ServiceUpdate, ServiceOut


class VendorRepository(ABC):
    @abstractmethod
    def create(self, data: VendorCreate) -> VendorOut: ...

    @abstractmethod
    def get(self, vendor_id: int) -> Optional[VendorOut]: ...

    @abstractmethod
    def list(self, limit: int, offset: int) -> List[VendorOut]: ...

    @abstractmethod
    def count(self) -> int: ...

    @abstractmethod
    def update(self, vendor_id: int, data: VendorUpdate) -> Optional[VendorOut]: ...

    @abstractmethod
    def delete(self, vendor_id: int) -> bool: ...

    @abstractmethod
    def list_with_active_services(self, limit: int, offset: int) -> List[VendorWithActiveServices]: ...


class ServiceContractRepository(ABC):
    @abstractmethod
    def create_for_vendor(self, vendor_id: int, data: ServiceCreate) -> ServiceOut: ...

    @abstractmethod
    def get(self, service_id: int) -> Optional[ServiceOut]: ...

    @abstractmethod
    def list_for_vendor(self, vendor_id: int, limit: int, offset: int) -> List[ServiceOut]: ...

    @abstractmethod
    def update(self, service_id: int, data: ServiceUpdate) -> Optional[ServiceOut]: ...

    @abstractmethod
    def delete(self, service_id: int) -> bool: ...

    @abstractmethod
    def list_expiring_before(self, cutoff: date, limit: int, offset: int) -> List[ServiceOut]: ...

    @abstractmethod
    def list_payment_due_before(self, cutoff: date, limit: int, offset: int) -> List[ServiceOut]: ...


