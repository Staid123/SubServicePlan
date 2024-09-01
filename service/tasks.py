from celery import Celery

from database.models import Plan, Service


celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)

@celery_app.task
def set_price(plan: Plan, service: Service) -> int:
    price = (
        service.full_price - service.full_price * (plan.discount_percent / 100)
    )
    return price