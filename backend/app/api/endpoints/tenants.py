"""
Tenant API endpoints
"""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_async_session
from app.models.tenant import Tenant as TenantModel
from app.schemas.tenant import Tenant, TenantCreate, TenantUpdate

router = APIRouter()


@router.get("/", response_model=List[Tenant])
async def get_tenants(
    session: AsyncSession = Depends(get_async_session),
):
    """Get all tenants"""
    result = await session.execute(select(TenantModel))
    tenants = result.scalars().all()
    return [Tenant.model_validate(tenant) for tenant in tenants]


@router.get("/{tenant_id}", response_model=Tenant)
async def get_tenant(
    tenant_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """Get tenant by ID"""
    result = await session.execute(
        select(TenantModel).where(TenantModel.id == tenant_id)
    )
    tenant = result.scalar_one_or_none()
    
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return Tenant.model_validate(tenant)


@router.post("/", response_model=Tenant)
async def create_tenant(
    tenant: TenantCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Create new tenant"""
    tenant_model = TenantModel(**tenant.model_dump())
    session.add(tenant_model)
    await session.commit()
    await session.refresh(tenant_model)
    
    return Tenant.model_validate(tenant_model)