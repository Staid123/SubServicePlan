from typing import Annotated
from fastapi import APIRouter, Query, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import session_getter
from subscription.service.subscription_service import SubscriptionService, get_subscription_service
from subscription.schemas import SubscriptionIn, SubscriptionOut


router = APIRouter(
    prefix="/subscription", 
    tags=["Subscription Operations"],
)


@router.get("/subs/{user_id}/", summary="Get user subscriptions")
async def get_all_user_subscriptions(
    user_id: int,
    subscription_service: Annotated[SubscriptionService, Depends(get_subscription_service)],
    session: Annotated[AsyncSession, Depends(session_getter)],
    skip: int = Query(default=0, ge=0), 
    limit: int = Query(default=10, ge=1),
):
    return await subscription_service.list_subscriptions(
        user_id=user_id,
        session=session,
        skip=skip,
        limit=limit,
    )


@router.post("/", response_model=SubscriptionOut, status_code=status.HTTP_201_CREATED)
async def create_subscription(
    subscription_in: SubscriptionIn,
    subscription_service: Annotated[SubscriptionService, Depends(get_subscription_service)],
    session: Annotated[AsyncSession, Depends(session_getter)],
) -> SubscriptionOut:
    return await subscription_service.create_subscription(
        session=session,
        subscription_in=subscription_in
    )


@router.delete("/{subscription_id}/", status_code=status.HTTP_204_NO_CONTENT)
async def update_subscription(
    subscription_service: Annotated[SubscriptionService, Depends(get_subscription_service)],
    session: Annotated[AsyncSession, Depends(session_getter)],
    subscription_id: int
) -> None:
    return await subscription_service.delete_subscription(
        session=session,
        subscription_id=subscription_id
    )