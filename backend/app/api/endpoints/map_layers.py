"""
Map Layer API endpoints
"""
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_async_session
from app.models.map_layer import MapLayer as MapLayerModel
from app.models.tenant import Tenant as TenantModel
from app.schemas.map_layer import MapLayer, MapLayerCreate, MapLayerUpdate

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


@router.get("/", response_model=List[MapLayer])
async def get_map_layers(
    session: AsyncSession = Depends(get_async_session),
):
    """Get all map layers for default tenant"""
    try:
        tenant = await get_default_tenant(session)
        
        result = await session.execute(
            select(MapLayerModel).where(MapLayerModel.tenant_id == tenant.id)
            .order_by(MapLayerModel.z_index)
        )
        layers = result.scalars().all()
        return [MapLayer.model_validate(layer) for layer in layers]
    except HTTPException:
        # If no default tenant, return empty list instead of hanging
        return []


@router.post("/", response_model=MapLayer)
async def create_map_layer(
    map_layer: MapLayerCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Create new map layer"""
    tenant = await get_default_tenant(session)
    
    layer_dict = map_layer.model_dump()
    layer_dict["tenant_id"] = tenant.id
    
    layer_model = MapLayerModel(**layer_dict)
    session.add(layer_model)
    await session.commit()
    await session.refresh(layer_model)
    
    return MapLayer.model_validate(layer_model)


@router.patch("/{layer_id}", response_model=MapLayer)
async def update_map_layer(
    layer_id: UUID,
    layer_update: MapLayerUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Update map layer"""
    tenant = await get_default_tenant(session)
    
    result = await session.execute(
        select(MapLayerModel).where(
            MapLayerModel.id == layer_id,
            MapLayerModel.tenant_id == tenant.id
        )
    )
    layer = result.scalar_one_or_none()
    
    if not layer:
        raise HTTPException(status_code=404, detail="Map layer not found")
    
    for field, value in layer_update.model_dump(exclude_unset=True).items():
        setattr(layer, field, value)
    
    await session.commit()
    await session.refresh(layer)
    
    return MapLayer.model_validate(layer)