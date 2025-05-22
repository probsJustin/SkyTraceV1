"""
Data Source API endpoints
"""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_async_session
from app.models.data_source import DataSource as DataSourceModel
from app.models.tenant import Tenant as TenantModel
from app.schemas.data_source import DataSource, DataSourceCreate, DataSourceUpdate

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


@router.get("/", response_model=List[DataSource])
async def get_data_sources(
    session: AsyncSession = Depends(get_async_session),
):
    """Get all data sources for default tenant"""
    tenant = await get_default_tenant(session)
    
    result = await session.execute(
        select(DataSourceModel).where(DataSourceModel.tenant_id == tenant.id)
    )
    sources = result.scalars().all()
    return [DataSource.model_validate(source) for source in sources]


@router.post("/", response_model=DataSource)
async def create_data_source(
    data_source: DataSourceCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Create new data source"""
    tenant = await get_default_tenant(session)
    
    source_dict = data_source.model_dump()
    source_dict["tenant_id"] = tenant.id
    
    source_model = DataSourceModel(**source_dict)
    session.add(source_model)
    await session.commit()
    await session.refresh(source_model)
    
    return DataSource.model_validate(source_model)


@router.get("/{source_id}", response_model=DataSource)
async def get_data_source(
    source_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """Get data source by ID"""
    tenant = await get_default_tenant(session)
    
    result = await session.execute(
        select(DataSourceModel).where(
            DataSourceModel.id == source_id,
            DataSourceModel.tenant_id == tenant.id
        )
    )
    source = result.scalar_one_or_none()
    
    if not source:
        raise HTTPException(status_code=404, detail="Data source not found")
    
    return DataSource.model_validate(source)