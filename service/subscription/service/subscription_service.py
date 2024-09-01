from database.models import Plan, Service, Subscription
from tasks import set_price
from subscription.repository.subscription_repository import SubscriptionRepository
from subscription.schemas import SubscriptionIn, SubscriptionOut
from subscription.repository.service_repository import ServiceRepository
from subscription.repository.plan_repository import PlanRepository
from sqlalchemy.ext.asyncio import AsyncSession


class SubscriptionService:
    def __init__(
            self, 
            subscription_repository: SubscriptionRepository,
            plan_repository: PlanRepository,
            service_repository: ServiceRepository
        ):
        """
        Initialize the subscription service with a subscription plan service repositories.
        """
        self.subscription_repository = subscription_repository
        self.plan_repository = plan_repository
        self.service_repository = service_repository

    
    async def create_subscription(
        self,
        subscription_in: SubscriptionIn,
        session: AsyncSession
    ) -> SubscriptionOut:
        plan: Plan = await self.plan_repository.get_plan_by_id(
            session=session,
            plan_id=subscription_in.plan_id
        )
        service: Service = await self.service_repository.get_service_by_id(
            session=session,
            service_id=subscription_in.service_id
        )
        price: int = set_price.delay(plan, service)
        subscription: Subscription = await self.subscription_repository.create_subscription(
            session=session,
            subscription_in=subscription_in,
            price=price,
        )
        return SubscriptionOut.model_validate(subscription, from_attributes=True)


def get_subscription_service():
    return SubscriptionService(SubscriptionRepository, PlanRepository, ServiceRepository)