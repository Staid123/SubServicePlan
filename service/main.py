from fastapi import FastAPI
from subscription.routers import router


app = FastAPI(
    title="SubServicePlan API",
)

app.include_router(router)
# app.include_router(auth_router)

