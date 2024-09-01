from typing import Annotated
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import session_getter
from subscription.service.subscription_service import SubscriptionService, get_subscription_service
from subscription.schemas import SubscriptionIn, SubscriptionOut


router = APIRouter(
    prefix="/subscription", 
    tags=["Subscription Operations"],
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