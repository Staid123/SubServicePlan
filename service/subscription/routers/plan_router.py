from typing import Annotated, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from enums import PlanType
from database import session_getter
from subscription.service.plan_service import PlanService, get_plan_service
from subscription.schemas import PlanIn, PlanOut, PlanUpdate


router = APIRouter(
    prefix="/plan", 
    tags=["Plan Operations"],
)

@router.get("/all/", response_model=list[PlanOut])
async def get_all_plans(
    plan_service: Annotated[PlanService, Depends(get_plan_service)],
    session: Annotated[AsyncSession, Depends(session_getter)],
    skip: int = Query(default=0, ge=0), 
    limit: int = Query(default=10, ge=1),
    plan_type: Optional[PlanType] = Query(default=None),
) -> list[PlanOut]:
    return await plan_service.list_plans(
        session=session,
        plan_type=plan_type,
        skip=skip,
        limit=limit,
    )

@router.get("/{plan_id}/", response_model=PlanOut)
async def get_plan_by_id(
    plan_service: Annotated[PlanService, Depends(get_plan_service)],
    session: Annotated[AsyncSession, Depends(session_getter)],
    plan_id: int
) -> PlanOut:
    return await plan_service.get_plan_by_id(
        session=session,
        plan_id=plan_id
    )

@router.post("/", response_model=PlanOut, status_code=status.HTTP_201_CREATED)
async def create_plan(
    plan_in: PlanIn,
    plan_service: Annotated[PlanService, Depends(get_plan_service)],
    session: Annotated[AsyncSession, Depends(session_getter)],
) -> PlanOut:
    return await plan_service.create_plan(
        session=session,
        plan_in=plan_in
    )

@router.patch("/{plan_id}/", response_model=PlanOut)
async def update_plan(
    plan_update: PlanUpdate,
    plan_service: Annotated[PlanService, Depends(get_plan_service)],
    session: Annotated[AsyncSession, Depends(session_getter)],
    plan_id: int
) -> PlanOut:
    return await plan_service.update_plan(
        session=session,
        plan_update=plan_update,
        plan_id=plan_id
    )