from fastapi import HTTPException
from sqlalchemy import select
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from sqlalchemy.orm import joinedload
from enums import PlanType
from database.models import Plan
from subscription.schemas import PlanIn, PlanOut, PlanUpdate


class PlanRepository:
    async def list_plans(
        self, 
        session: AsyncSession, 
        plan_type: Optional[PlanType],
        skip: int,
        limit: int,
    ) -> list[Plan]:
        stmt = (
            select(Plan)
            .options(
                joinedload(Plan.subscriptions),
            )
            .offset(skip)
            .limit(limit)
            .order_by(Plan.id)
        )
        if plan_type:
            stmt.filter_by(plan_type=plan_type)
        plans: list[Plan] = await session.scalars(stmt)
        return plans.all()
    
    async def get_plan_by_id(
        self,
        session: AsyncSession,
        plan_id: int
    ) -> Plan:
        plan = await session.get(Plan, plan_id)
        if plan:
            return plan
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found"
        )
    
    async def create_plan(
        self,
        session: AsyncSession,
        plan_in: PlanIn
    ) -> PlanOut:
        # try:
            plan: Plan = Plan(**plan_in.model_dump())
            session.add(plan)
            await session.commit()
            return await self.get_plan_by_id(session=session, plan_id=plan.id)
        # except Exception:
        #     await session.rollback()
        #     raise HTTPException(
        #         status_code=status.HTTP_400_BAD_REQUEST,
        #         detail="Can not add plan"
        #     )
        
    async def update_plan(
        self,
        session: AsyncSession,
        plan_update: PlanUpdate,
        plan_id: int
    ) -> PlanOut:
        plan: Plan = await self.get_plan_by_id(
            session=session,
            plan_id=plan_id
        )
        try:
            for name, value in plan_update.model_dump(exclude_none=True).items():
                setattr(plan, name, value)
            await session.commit()
            return plan
        except Exception:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not update plan"
            )