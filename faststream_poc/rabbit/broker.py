from typing import Annotated

from fastapi import Depends
from faststream.rabbit import RabbitBroker

from faststream_poc.settings import settings

rabbit_broker = RabbitBroker(
    settings.rabbit_url,
    asyncapi_url='asyncdoc'
)


def get_broker():
    return rabbit_broker


Broker = Annotated[RabbitBroker, Depends(get_broker)]
