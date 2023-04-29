import asyncio

from src.worker.broker.rabbitmq import RabbitMQ
from src.core.settings import rabbit_settings


if __name__ == "__main__":
    asyncio.run(RabbitMQ().consume(rabbit_settings.queue_email, rabbit_settings.exchange, 'email.auto.best_movies'))
    asyncio.run(RabbitMQ().consume(rabbit_settings.queue_email, rabbit_settings.exchange, 'email.admin.any'))
    asyncio.run(RabbitMQ().consume(rabbit_settings.queue_email, rabbit_settings.exchange, 'email.service'))
