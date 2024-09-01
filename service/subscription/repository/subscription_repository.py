from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Subscription
from subscription.schemas import SubscriptionIn


class SubscriptionRepository:
    async def get_subscription_by_id(
        self,
        session: AsyncSession,
        subscription_id: int
    ) -> Subscription:
        subscription = await session.get(Subscription, subscription_id)
        if subscription:
            return subscription
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    
    async def create_subscription(
        self,
        session: AsyncSession,
        subscription_in: SubscriptionIn,
        price: int,
    ) -> Subscription:
        try:
            subscription_in_to_dict: dict = subscription_in.model_dump().update({"price": price})
            subscription: Subscription = Subscription(**subscription_in_to_dict)
            session.add(subscription)
            await session.commit()
            return await self.get_subscription_by_id(
                session=session,
                subscription_id=subscription.id
            )
        except Exception:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not add subscription"
            )
