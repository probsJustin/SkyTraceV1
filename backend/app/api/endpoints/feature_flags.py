"""
Feature Flag API endpoints
"""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_async_session
from app.models.feature_flag import FeatureFlag as FeatureFlagModel
from app.models.tenant import Tenant as TenantModel
from app.schemas.feature_flag import FeatureFlag, FeatureFlagCreate, FeatureFlagUpdate

router = APIRouter()


async def get_default_tenant(session: AsyncSession) -> TenantModel:
    """Get default tenant"""
    result = await session.execute(
        select(TenantModel).where(TenantModel.slug == "default")
    )
    tenant = result.scalar_one_or_none()
    if not tenant:
        raise HTTPException(status_code=404, detail="Default tenant not found")
    return tenant


@router.get("/", response_model=List[FeatureFlag])
async def get_feature_flags(
    session: AsyncSession = Depends(get_async_session),
):
    """Get all feature flags for default tenant"""
    tenant = await get_default_tenant(session)
    
    result = await session.execute(
        select(FeatureFlagModel).where(FeatureFlagModel.tenant_id == tenant.id)
    )
    flags = result.scalars().all()
    return [FeatureFlag.model_validate(flag) for flag in flags]


@router.patch("/{flag_name}", response_model=FeatureFlag)
async def update_feature_flag(
    flag_name: str,
    flag_update: FeatureFlagUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Update feature flag"""
    tenant = await get_default_tenant(session)
    
    result = await session.execute(
        select(FeatureFlagModel).where(
            FeatureFlagModel.tenant_id == tenant.id,
            FeatureFlagModel.name == flag_name
        )
    )
    flag = result.scalar_one_or_none()
    
    if not flag:
        raise HTTPException(status_code=404, detail="Feature flag not found")
    
    for field, value in flag_update.model_dump(exclude_unset=True).items():
        setattr(flag, field, value)
    
    await session.commit()
    await session.refresh(flag)
    
    return FeatureFlag.model_validate(flag)