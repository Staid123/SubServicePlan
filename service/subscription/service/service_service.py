from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Service
from subscription.schemas import ServiceIn, ServiceOut, ServiceUpdate
from subscription.repository.service_repository import ServiceRepository



class ServiceService:
    def __init__(self, service_repository: ServiceRepository):
        """
        Initialize the service service with a service repository.
        """
        self.service_repository = service_repository

    async def list_services(
        self, 
        session: AsyncSession, 
        skip: int,
        limit: int,
        name: str,
        full_price: int
    ) -> list[ServiceOut]:
        services: list[Service] = await self.service_repository.list_services(
            session=session, 
            name=name,
            full_price=full_price,
            skip=skip,
            limit=limit,
        )
        return [ServiceOut.model_validate(service, from_attributes=True) for service in services]
    
    async def get_service_by_id(
        self,
        session: AsyncSession,
        service_id: int
    ) -> ServiceOut:
        service: Service = await self.service_repository.get_service_by_id(
            session=session,
            service_id=service_id
        )
        return ServiceOut.model_validate(service, from_attributes=True)
    
    async def create_service(
        self,
        session: AsyncSession,
        service_in: ServiceIn
    ) -> ServiceOut:
        service: Service = await self.service_repository.create_service(
            session=session,
            service_in=service_in
        )
        return ServiceOut.model_validate(service, from_attributes=True)

    async def update_service(
        self,
        service_update: ServiceUpdate,
        session: AsyncSession,
        service_id: int
    ) -> ServiceUpdate:
        service: Service = await self.service_repository.update_service(
            session=session,
            service_update=service_update,
            service_id=service_id
        )
        return ServiceOut.model_validate(service, from_attributes=True)

    async def delete_service(
        self,
        service_id: int,
        session: AsyncSession
    ) -> None:
        return await self.service_repository.delete_service(
            session=session,
            service_id=service_id
        )


def get_service_service():
    return ServiceService(ServiceRepository())