from fastapi import APIRouter, Depends
# from fastapi.security import HTTPBearer
from subscription.routers.plan_router import router as plan_router
from subscription.routers.service_router import router as service_router
from subscription.routers.subscription_router import router as subscription_router


# интерфейс для введения токена (который автоматически отправляеятся в заголовки) после логина
# http_bearer = HTTPBearer(auto_error=False)

# router = APIRouter(dependencies=[Depends(http_bearer)])
router = APIRouter(prefix="/api/v1")


router.include_router(plan_router)
router.include_router(service_router)
router.include_router(subscription_router)
