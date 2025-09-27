from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from app.services.deps import get_current_user
from app.schemas.models import VendorCreate, VendorOut, VendorUpdate, PaginatedResponse, VendorWithActiveServices
from app.application.services import VendorService
from app.infrastructure.providers import get_vendor_service


router = APIRouter(prefix="/vendors", tags=["vendors"]) 


@router.post("/", response_model=VendorOut)
def create_vendor(
    vendor_in: VendorCreate,
    svc: VendorService = Depends(get_vendor_service),
    user=Depends(get_current_user),
):
    return svc.create_vendor(vendor_in)


@router.get("/", response_model=List[VendorOut])
def list_vendors(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    svc: VendorService = Depends(get_vendor_service),
    user=Depends(get_current_user),
):
    return svc.list_vendors(limit, offset)


@router.get("/count", response_model=PaginatedResponse)
def vendors_count(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    svc: VendorService = Depends(get_vendor_service),
    user=Depends(get_current_user),
):
    total = svc.count_vendors()
    return PaginatedResponse(total=total, limit=limit, offset=offset)


@router.get("/with-active-services", response_model=List[VendorWithActiveServices])
def list_vendors_with_active_services(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    svc: VendorService = Depends(get_vendor_service),
    user=Depends(get_current_user),
):
    return svc.list_vendors_with_active_services(limit, offset)


@router.get("/{vendor_id}", response_model=VendorOut)
def get_vendor(
    vendor_id: int,
    svc: VendorService = Depends(get_vendor_service),
    user=Depends(get_current_user),
):
    vendor = svc.get_vendor(vendor_id)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor


@router.put("/{vendor_id}", response_model=VendorOut)
def update_vendor(
    vendor_id: int,
    vendor_in: VendorUpdate,
    svc: VendorService = Depends(get_vendor_service),
    user=Depends(get_current_user),
):
    vendor = svc.update_vendor(vendor_id, vendor_in)
    if not vendor:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return vendor


@router.delete("/{vendor_id}", status_code=204)
def delete_vendor(
    vendor_id: int,
    svc: VendorService = Depends(get_vendor_service),
    user=Depends(get_current_user),
):
    ok = svc.delete_vendor(vendor_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return None


