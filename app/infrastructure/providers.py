from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..application.services import VendorService, ServiceContractService
from .repositories import SqlAlchemyVendorRepository, SqlAlchemyServiceContractRepository


def get_vendor_service(db: Session = Depends(get_db)) -> VendorService:
    return VendorService(vendor_repo=SqlAlchemyVendorRepository(db))


def get_service_contract_service(db: Session = Depends(get_db)) -> ServiceContractService:
    return ServiceContractService(service_repo=SqlAlchemyServiceContractRepository(db))


