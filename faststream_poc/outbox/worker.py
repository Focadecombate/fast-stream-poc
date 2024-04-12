import asyncio
import json
import logging
from datetime import datetime

from faststream.rabbit import RabbitBroker
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from faststream_poc.database.engine import async_session
from faststream_poc.database.models import HealthCheckOutBox
from faststream_poc.rabbit.exchanges import health_exchange
from faststream_poc.settings import settings

broker = RabbitBroker(
    url=settings.rabbit_url,
)

logger = logging.getLogger(__name__)


async def load_health_outbox(session: AsyncSession):
    async with async_session() as session:
        outbox_query = (
            select(HealthCheckOutBox)
            .where(HealthCheckOutBox.send_at.is_(None))
            .order_by(HealthCheckOutBox.created_at)
        )

        result = await session.execute(outbox_query)

        return result.scalars().all()


async def send_outbox():
    async with async_session() as session:
        outbox = await load_health_outbox(session)
        if not outbox:
            await session.close()
            return
        logger.info(
            "Sending health outbox - {count} messages".format(count=len(outbox))
        )
        for message in outbox:
            await broker.publish(
                exchange=health_exchange,
                routing_key=message.event_type,
                message=json.loads(message.message),
            )
            message.send_at = datetime.utcnow()
            session.add(message)
        await session.commit()


async def main():
    try:
        await broker.connect()
        logger.info("Starting outbox worker")
        while True:
            await send_outbox()
            await asyncio.sleep(2)
    except Exception as e:
        logger.error("Error sending health outbox", exc_info=e)

    finally:
        await broker.close()


if __name__ == "__main__":
    asyncio.run(main())
