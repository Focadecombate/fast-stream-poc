from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column


class Base(DeclarativeBase, MappedAsDataclass):
    pass


class HealthCheck(Base):
    __tablename__ = "health_check"

    id: Mapped[str] = mapped_column(primary_key=True)
    event: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=datetime.utcnow
    )


class HealthCheckOutBox(Base):
    __tablename__ = "health_check_outbox"

    id: Mapped[str] = mapped_column(primary_key=True)
    message: Mapped[str] = mapped_column()
    event_type: Mapped[str] = mapped_column()
    send_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=datetime.utcnow
    )
