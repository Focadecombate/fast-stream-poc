import logging

from faststream import FastStream

from faststream_poc.rabbit.broker import rabbit_broker
from faststream_poc.rabbit.consumers.health import router

logging.basicConfig(level="INFO")

rabbit_broker.include_router(router)
app = FastStream(rabbit_broker)
