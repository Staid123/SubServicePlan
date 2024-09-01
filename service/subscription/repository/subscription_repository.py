from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Subscription
from subscription.schemas import SubscriptionIn
from sqlalchemy.orm import joinedload


class SubscriptionRepository:
    async def get_subscription_by_id(
        self,
        session: AsyncSession,
        subscription_id: int
    ) -> Subscription:
        stmt = (
            select(Subscription)
            .options(
                joinedload(Subscription.user),
                joinedload(Subscription.service),
                joinedload(Subscription.plan),
            )
            .filter_by(id=subscription_id)
        )
        sub_with_options: Subscription = await session.scalars(stmt)
        if sub_with_options:
            return sub_with_options.one()
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
            data = subscription_in.model_dump()
            data["price"] = price
            subscription: Subscription = Subscription(**data)
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

    async def list_subscriptions(
        self,
        session: AsyncSession,
        user_id: int,
        skip: int, 
        limit: int, 
    ) -> list[Subscription]:
        stmt = (
            select(Subscription)
            .options(
                joinedload(Subscription.user),
                joinedload(Subscription.service),
                joinedload(Subscription.plan),
            )
            .filter_by(user_id=user_id)
            .offset(skip)
            .limit(limit)
            .order_by(Subscription.id)
        )
        subscriptions: list[Subscription] = await session.scalars(stmt)
        return subscriptions.all()
    
    async def delete_subscription(
        self,
        session: AsyncSession,
        subscription_id: int
    ) -> None:
        subscription: Subscription = await self.get_subscription_by_id(
            session=session,
            subscription_id=subscription_id
        )
        try:
            await session.delete(subscription)
            await session.commit()
        except Exception:
            await session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can not delete subscription"
            )