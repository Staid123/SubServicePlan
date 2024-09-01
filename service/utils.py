from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Plan, Service

    
async def set_price(session: AsyncSession, plan_id: int, service_id: int) -> int:
    plan = await session.get(Plan, plan_id)
    service = await session.get(Service, service_id)
    price = (
        service.full_price - service.full_price * (plan.discount_percent / 100)
    )
    return int(price)


async def set_total_price(subscriptions: dict):
    return sum(map(lambda item: item['price'], subscriptions))