from faststream.rabbit import ExchangeType, RabbitExchange

health_dlx_exchange = RabbitExchange(
    name="health-dlx",
    type=ExchangeType.TOPIC,
    durable=True,
    auto_delete=False,
    arguments={
        "x-message-ttl": 10000,
    },
)

health_exchange = RabbitExchange(
    name="health",
    type=ExchangeType.TOPIC,
    durable=True,
    auto_delete=False,
    arguments={
        "x-dead-letter-exchange": health_dlx_exchange.name,
    },
)
