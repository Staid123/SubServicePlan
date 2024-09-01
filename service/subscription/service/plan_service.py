from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from enums import PlanType
from database.models import Plan
from redis_cache import RedisCache
from subscription.schemas import PlanIn, PlanOut, PlanUpdate
from subscription.repository.plan_repository import PlanRepository



class PlanService:
    TOTAL_PRICE = "total_price"

    def __init__(self, plan_repository: PlanRepository):
        """
        Initialize the plan service with a plan repository.
        """
        self.plan_repository = plan_repository

    async def list_plans(
        self, 
        session: AsyncSession, 
        plan_type: Optional[PlanType],
        skip: int,
        limit: int,
    ) -> list[PlanOut]:
        plans: list[Plan] = await self.plan_repository.list_plans(
            session=session, 
            plan_type=plan_type,
            skip=skip,
            limit=limit,
        )
        return [PlanOut.model_validate(plan, from_attributes=True) for plan in plans]
    
    async def get_plan_by_id(
        self,
        session: AsyncSession,
        plan_id: int
    ) -> PlanOut:
        plan: Plan = await self.plan_repository.get_plan_by_id(
            session=session,
            plan_id=plan_id
        )
        return PlanOut.model_validate(plan, from_attributes=True)
    
    async def create_plan(
        self,
        session: AsyncSession,
        plan_in: PlanIn
    ) -> PlanOut:
        plan: Plan = await self.plan_repository.create_plan(
            session=session,
            plan_in=plan_in
        )
        return PlanOut.model_validate(plan, from_attributes=True)

    async def update_plan(
        self,
        plan_update: PlanUpdate,
        session: AsyncSession,
        plan_id: int,
        redis_cache: RedisCache
    ) -> PlanUpdate:
        plan: Plan = await self.plan_repository.update_plan(
            session=session,
            plan_update=plan_update,
            plan_id=plan_id
        )
        await redis_cache.delete(self.TOTAL_PRICE)
        return PlanOut.model_validate(plan, from_attributes=True)

    async def delete_plan(
        self,
        plan_id: int,
        session: AsyncSession,
        redis_cache: RedisCache
    ) -> None:
        await self.plan_repository.delete_plan(
            session=session,
            plan_id=plan_id
        )
        await redis_cache.delete(self.TOTAL_PRICE)
        return None



def get_plan_service():
    return PlanService(PlanRepository())