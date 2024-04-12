from faststream.rabbit import RabbitBroker

from faststream_poc.settings import settings

rabbit_broker = RabbitBroker(
    settings.rabbit_url,
)
