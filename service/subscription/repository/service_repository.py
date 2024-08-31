from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from database.models import Service
from subscription.schemas import ServiceIn, ServiceOut, ServiceUpdate


class ServiceRepository:
    async def list_services(
        self, 
        session: AsyncSession, 
        skip: int,
        limit: int,
        name: str,
        full_price: int
    ) -> list[Service]:
        stmt = (
            select(Service)
            .offset(skip)
            .limit(limit)
            .order_by(Service.id)
        )
        if name:
            stmt.filter_by(name=name)
        if full_price:
            stmt.filter_by(full_price=full_price)
        services: list[Service] = await session.scalars(stmt)
        return services.all()
    
    async def get_service_by_id(
        self,
        session: AsyncSession,
        service_id: int
    ) -> Service:
        service = await session.get(Service, service_id)
        if service:
            return service
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    async def create_service(
        self,
        session: AsyncSession,
        service_in: ServiceIn
    ) -> ServiceOut:
        try:
            service: Service = Service(**service_in.model_dump())
            session.add(service)
            await session.commit()
            return await self.get_service_by_id(session=session, service_id=service.id)
        except Exception:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not add service"
            )
        
    async def update_service(
        self,
        session: AsyncSession,
        service_update: ServiceUpdate,
        service_id: int
    ) -> ServiceOut:
        service: Service = await self.get_service_by_id(
            session=session,
            service_id=service_id
        )
        try:
            for name, value in service_update.model_dump(exclude_none=True).items():
                setattr(service, name, value)
            await session.commit()
            return service
        except Exception:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not update service"
            )
        
    async def delete_service(
        self,
        session: AsyncSession,
        service_id: int
    ) -> None:
        service: Service = await self.get_service_by_id(
            session=session,
            service_id=service_id
        )
        try:
            await session.delete(service)
            await session.commit()
        except Exception:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not delete service"
            )