from typing import Annotated
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import session_getter
from redis_cache import RedisCache, get_redis_helper
from subscription.service.service_service import ServiceService, get_service_service
from subscription.schemas import ServiceIn, ServiceOut, ServiceUpdate


router = APIRouter(
    prefix="/service", 
    tags=["Service Operations"],
)


@router.get("/all/", response_model=list[ServiceOut])
async def get_all_services(
    service_service: Annotated[ServiceService, Depends(get_service_service)],
    session: Annotated[AsyncSession, Depends(session_getter)],
    skip: int = Query(default=0, ge=0), 
    limit: int = Query(default=10, ge=1),
    name: str = Query(default=None),
    full_price: int = Query(default=None, ge=1)
) -> list[ServiceOut]:
    return await service_service.list_services(
        session=session,
        skip=skip,
        limit=limit,
        name=name,
        full_price=full_price
    )

@router.get("/{service_id}/", response_model=ServiceOut)
async def get_service_by_id(
    service_service: Annotated[ServiceService, Depends(get_service_service)],
    session: Annotated[AsyncSession, Depends(session_getter)],
    service_id: int
) -> ServiceOut:
    return await service_service.get_service_by_id(
        session=session,
        service_id=service_id
    )

@router.post("/", response_model=ServiceOut, status_code=status.HTTP_201_CREATED)
async def create_service(
    service_in: ServiceIn,
    service_service: Annotated[ServiceService, Depends(get_service_service)],
    session: Annotated[AsyncSession, Depends(session_getter)],
) -> ServiceOut:
    return await service_service.create_service(
        session=session,
        service_in=service_in
    )

@router.patch("/{service_id}/", response_model=ServiceOut)
async def update_service(
    service_update: ServiceUpdate,
    service_service: Annotated[ServiceService, Depends(get_service_service)],
    session: Annotated[AsyncSession, Depends(session_getter)],
    redis_helper: Annotated[RedisCache, Depends(get_redis_helper)],
    service_id: int
) -> ServiceOut:
    return await service_service.update_service(
        session=session,
        service_update=service_update,
        service_id=service_id,
        redis_helper=redis_helper,
    )

@router.delete("/{service_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_service(
    service_id: int,
    service_service: Annotated[ServiceService, Depends(get_service_service)],
    session: Annotated[AsyncSession, Depends(session_getter)],
    redis_helper: Annotated[RedisCache, Depends(get_redis_helper)],
) -> None:
    return await service_service.delete_service(
        session=session,
        service_id=service_id,
        redis_helper=redis_helper
    )