import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from faststream_poc.api.health import router as health_router
from faststream_poc.database.engine import init_db
from faststream_poc.outbox import worker
from faststream_poc.rabbit.broker import rabbit_broker
from faststream_poc.settings import settings

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.settings = settings
    await rabbit_broker.connect()
    outbox_task = asyncio.create_task(worker.main())
    await init_db()
    yield
    await rabbit_broker.close()
    outbox_task.cancel()
    await asyncio.wait([outbox_task])


app = FastAPI(
    title="FastStream POC",
    description="FastStream POC",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health_router)
