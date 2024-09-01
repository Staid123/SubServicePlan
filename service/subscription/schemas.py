from datetime import datetime
from typing import Optional
from pydantic import ConfigDict, BaseModel, EmailStr

from enums import PlanType


class ServiceBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    full_price: int

class ServiceIn(ServiceBase):
    pass

class ServiceOut(ServiceIn):
    id: int

class ServiceUpdate(BaseModel):
    name: str | None = None
    full_price: int | None = None


class PlanBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    plan_type: PlanType
    discount_percent: int

class PlanIn(PlanBase):
    pass

class PlanOut(PlanIn):
    id: int

class PlanUpdate(BaseModel):
    discount_percent: int | None = None


class SubscriptionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    service_id: int
    plan_id: int

class SubscriptionIn(SubscriptionBase):
    pass

class SubscriptionOut(SubscriptionIn):
    id: int

    created_at: datetime
    price: int
    user: "UserBase"
    service: "ServiceBase"
    plan: "PlanBase"

class SubscriptionUpdate(BaseModel):
    user_id: int | None = None
    service_id: int | None = None
    plan_id: int | None = None


class UserBase(BaseModel):
    username: str
    email: EmailStr
    password_hash: str
    active: bool