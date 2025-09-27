from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from app.services.deps import get_current_user
from app.application.services import ServiceContractService
from app.infrastructure.providers import get_service_contract_service
from app.schemas.models import ServiceCreate, ServiceOut, ServiceUpdate, ServiceStatusUpdate


router = APIRouter(prefix="/services", tags=["services"]) 


@router.post("/vendor/{vendor_id}", response_model=ServiceOut)
def create_service(
    vendor_id: int,
    service_in: ServiceCreate,
    svc: ServiceContractService = Depends(get_service_contract_service),
    user=Depends(get_current_user),
):
    s = svc.create_service(vendor_id, service_in)
    if not s:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return s


@router.get("/vendor/{vendor_id}", response_model=List[ServiceOut])
def list_services_for_vendor(
    vendor_id: int,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    svc: ServiceContractService = Depends(get_service_contract_service),
    user=Depends(get_current_user),
):
    return svc.list_services_for_vendor(vendor_id, limit, offset)


@router.put("/{service_id}", response_model=ServiceOut)
def update_service(
    service_id: int,
    service_in: ServiceUpdate,
    svc: ServiceContractService = Depends(get_service_contract_service),
    user=Depends(get_current_user),
):
    s = svc.update_service(service_id, service_in)
    if not s:
        raise HTTPException(status_code=404, detail="Service not found")
    return s


@router.delete("/{service_id}", status_code=204)
def delete_service(
    service_id: int,
    svc: ServiceContractService = Depends(get_service_contract_service),
    user=Depends(get_current_user),
):
    ok = svc.delete_service(service_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Service not found")
    return None


@router.post("/{service_id}/status", response_model=ServiceOut)
def update_service_status(
    service_id: int,
    status_in: ServiceStatusUpdate,
    svc: ServiceContractService = Depends(get_service_contract_service),
    user=Depends(get_current_user),
):
    s = svc.update_service_status(service_id, status_in.status)
    if not s:
        raise HTTPException(status_code=404, detail="Service not found")
    return s


@router.get("/expiring", response_model=List[ServiceOut])
def services_expiring_next_15_days(
    days: int = Query(15, ge=1, le=60),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    svc: ServiceContractService = Depends(get_service_contract_service),
    user=Depends(get_current_user),
):
    return svc.services_expiring(days, limit, offset)


@router.get("/payment-due", response_model=List[ServiceOut])
def services_payment_due_next_15_days(
    days: int = Query(15, ge=1, le=60),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    svc: ServiceContractService = Depends(get_service_contract_service),
    user=Depends(get_current_user),
):
    return svc.services_payment_due(days, limit, offset)


