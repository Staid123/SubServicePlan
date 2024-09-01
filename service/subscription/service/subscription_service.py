from database.models import Subscription
from utils import set_price, set_total_price
from subscription.repository.subscription_repository import SubscriptionRepository
from subscription.schemas import SubscriptionIn, SubscriptionOut
from subscription.repository.service_repository import ServiceRepository
from subscription.repository.plan_repository import PlanRepository
from sqlalchemy.ext.asyncio import AsyncSession


class SubscriptionService:
    def __init__(self, subscription_repository: SubscriptionRepository):
        """
        Initialize the subscription service with a subscription plan service repositories.
        """
        self.subscription_repository = subscription_repository
    
    async def create_subscription(
        self,
        subscription_in: SubscriptionIn,
        session: AsyncSession
    ) -> SubscriptionOut:
        price: int = await set_price(
            session=session,
            plan_id=subscription_in.plan_id, 
            service_id=subscription_in.service_id
        )
        subscription: Subscription = await self.subscription_repository.create_subscription(
            session=session,
            subscription_in=subscription_in,
            price=price,
        )
        return SubscriptionOut.model_validate(subscription, from_attributes=True)

    async def list_subscriptions(
        self,
        user_id: int,
        session: AsyncSession,
        skip: int,
        limit: int,
    ):
        subscriptions: list[Subscription] = await self.subscription_repository.list_subscriptions(
            user_id=user_id,
            session=session,
            skip=skip,
            limit=limit
        )
        subscriptions_dicts = [
            (SubscriptionOut.model_validate(subscription, from_attributes=True)).model_dump()
            for subscription in subscriptions
        ]
        total_price = await set_total_price(subscriptions_dicts) 
        # Добавление total_price к результату
        result = {
            "subscriptions": subscriptions_dicts,
            "total_price": total_price
        }
        return result


    async def delete_subscription(
        self,
        subscription_id: int,
        session: AsyncSession
    ) -> None:
        return await self.subscription_repository.delete_subscription(
            session=session,
            subscription_id=subscription_id
        )

def get_subscription_service():
    return SubscriptionService(SubscriptionRepository())