import logging

from faststream.rabbit import RabbitMessage, RabbitQueue, RabbitRouter

from faststream_poc.rabbit.exchanges import health_dlx_exchange, health_exchange
from faststream_poc.rabbit.message import HealthMessage

logger = logging.getLogger(__name__)


router = RabbitRouter(prefix="health_")


@router.subscriber(
    RabbitQueue(
        "ok",
        durable=True,
        routing_key="health.ok",
        arguments={
            "x-dead-letter-exchange": health_dlx_exchange.name,
        },
    ),
    health_exchange,
)
async def ok_health_consumer(body: HealthMessage, raw_message: RabbitMessage):
    logger.info(f"Health is ok {body}")
    await raw_message.ack()


@router.subscriber(
    RabbitQueue(
        "bad",
        durable=True,
        routing_key="health.bad",
        arguments={
            "x-dead-letter-exchange": health_dlx_exchange.name,
        },
    ),
    health_exchange,
)
async def bad_health_consumer(
    message_body: HealthMessage,
    raw_message: RabbitMessage,
):
    logger.error(f"Health is bad {message_body.event}")

    await raw_message.ack()


@router.subscriber(
    RabbitQueue(
        "check-log",
        durable=True,
        routing_key="health.*",
        arguments={
            "x-dead-letter-exchange": health_dlx_exchange.name,
        },
    ),
    health_exchange,
)
async def health_consumer(body: HealthMessage):
    logger.info("Health Check")


@router.subscriber(
    RabbitQueue(
        "error-in-check",
        durable=True,
        routing_key="*",
    ),
    health_dlx_exchange,
)
async def error_consumer(message: HealthMessage):
    logger.error(f"Error happened in message {message.id}")
