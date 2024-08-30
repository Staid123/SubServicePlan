from datetime import datetime
from sqlalchemy import TIMESTAMP, Boolean, CheckConstraint, ForeignKey, LargeBinary, UniqueConstraint, func
from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase,
    mapped_column,
    declared_attr,
    relationship
)
from enums import PlanType


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    

class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password_hash: Mapped[bytes] = mapped_column(LargeBinary)
    active: Mapped[bool] = mapped_column(Boolean, default=True, server_default='true')

    subscriptions: Mapped[list["Subscription"]] = relationship("Subscription", back_populates="user")



class Service(Base):
    name: Mapped[str] = mapped_column(unique=True)
    full_price: Mapped[int]

    service: Mapped[list["Subscription"]] = relationship("Subscription", back_populates="service")

    __table_args__ = (
        CheckConstraint('price > 0', name='check_price_positive'),
    )


class Plan(Base):
    plan_type: Mapped[PlanType]
    discount_percent: Mapped[int]

    subscriptions: Mapped[list["Subscription"]] = relationship("Subscription", back_populates="plan")

    __table_args__ = (
        CheckConstraint('discount_percent > 0', name='check_price_positive'),
    )


class Subscription(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"))
    plan_id: Mapped[int] = mapped_column(ForeignKey("plan.id"))
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())

    user: Mapped["User"] = relationship('User', back_populates='subscriptions')
    service: Mapped["Service"] = relationship('Service', back_populates='subscriptions')
    plan: Mapped["Plan"] = relationship("Plan", back_populates="subscriptions")

    __table_args__ = (
        UniqueConstraint("user_id", "service_id"),
    )