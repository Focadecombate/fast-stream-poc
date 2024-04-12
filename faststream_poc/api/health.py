from fastapi import APIRouter
from ulid import ulid

from faststream_poc.database.engine import Session
from faststream_poc.database.models import HealthCheck, HealthCheckOutBox
from faststream_poc.rabbit.broker import Broker
from faststream_poc.rabbit.exchanges import health_exchange
from faststream_poc.rabbit.message import HealthMessage

router = APIRouter(prefix="/health")


@router.get("/ok")
async def ok_health(session: Session):
    check_id = ulid()
    check = HealthCheck(id=check_id, event="Hello World")
    check_outbox = HealthCheckOutBox(
        id=check.id,
        message=HealthMessage(
            id=check_id, event="Some one entered /ok endpoint"
        ).model_dump_json(),
        event_type="health.ok",
    )
    session.add(check)
    session.add(check_outbox)
    await session.commit()
    return {"message": "ok"}


@router.get("/bad")
async def bad_health(broker: Broker):
    await broker.publish(
        exchange=health_exchange,
        routing_key="health.bad",
        message=HealthMessage(id=ulid()),
    )
    return {"message": "error"}
