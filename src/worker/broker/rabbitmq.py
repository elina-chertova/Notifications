import asyncio
import json
import time

from aio_pika import DeliveryMode, Message, connect
from aio_pika.abc import AbstractIncomingMessage

from generator.models.event import Event
from src.worker.broker.base import BaseQueue
from src.core.settings import Settings, logger
from src.worker.source.email.send_email import Email
from src.core.query import update_usr_nft
from src.storage.postgres import PSGR
from fastapi import Depends
from src.db.postgresdb import get_postgres
import asyncpg
from src.core.settings import psgr_settings


class RabbitMQ(BaseQueue):
    def __init__(self):
        self.settings = Settings()
        self.host = self.settings.rabbit_host
        self.login = self.settings.rabbit_login
        self.password = self.settings.rabbit_pswd

    async def declare(self, queue_name, exchange_name, exchange_type, routing_key):
        connection = await connect("amqp://{0}:{1}@{2}/".format(self.login,
                                                                self.password,
                                                                self.host))
        channel = await connection.channel()
        exchange = await channel.declare_exchange(name=exchange_name, type=exchange_type, durable=True)
        queue = await channel.declare_queue(queue_name)
        await queue.bind(exchange, routing_key)
        return connection, channel, exchange, queue

    async def produce(self,
                      msg,
                      queue_name: str,
                      exchange_name: str,
                      routing_key: str,
                      headers: dict = None,
                      exchange_type: str = 'direct'):

        _, _, exchange, _ = await self.declare(queue_name, exchange_name, exchange_type, routing_key)
        # queue_delay = await self.declare_delay(queue_name, exchange_name, exchange_type, routing_key)
        message = Message(headers=headers,
                          body=bytes(msg, 'utf-8'),
                          delivery_mode=DeliveryMode.PERSISTENT)
        await exchange.publish(message, routing_key)
        logger.info('Exchange name: {0}. Queue name: {1}. Sent message: {2}'.format(exchange_name, queue_name, message))
        time.sleep(0.01)

    async def choose_ntf_type(self, message: dict):
        if message['destination'] == 'Email':
            try:
                email_ = Email()
                email_.send(email=message['email'], subject=message['subject'], template=message['template'])
                email_.commit(message)
            except Exception as e:
                print('Error: ', e)

    async def on_message(self, message: AbstractIncomingMessage) -> None:
        await message.ack()
        event = Event(**json.loads(message.body)).dict()
        await self.choose_ntf_type(event)

    async def consume(self,
                      queue_name: str,
                      exchange_name: str,
                      routing_key: str,
                      exchange_type: str = 'direct'):

        connection, channel, _, queue = await self.declare(queue_name, exchange_name, exchange_type, routing_key)

        # async with connection:
        #     await channel.set_qos(prefetch_count=1)
        #     print(" [*] Waiting for logs. To exit press CTRL+C")
        #     await queue.consume(self.on_message, no_ack=False)
        #     await asyncio.Future()

        async with connection:
            await channel.set_qos(prefetch_count=1)
            print(" [*] Waiting for logs. To exit press CTRL+C")
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    event = Event(**json.loads(message.body)).dict()
                    await self.choose_ntf_type(event)
                    print('event on mess', event)
                    await message.ack()
#
# if __name__ == "__main__":
#     asyncio.run(RabbitMQ().consume('email_queue', 'exchange_not', 'auto.email.movies.month'))

    # async def declare_delay(self, queue_name, exchange_name, routing_key):
    #     connection = await connect("amqp://{0}:{1}@{2}/".format(self.login,
    #                                                             self.password,
    #                                                             self.host))
    #     channel = await connection.channel()
    #     delay_queue = queue_name + '_delay'
    #     queue = await channel.declare_queue(delay_queue, durable=True, arguments={
    #         'x-message-ttl': 5500,
    #         'x-dead-letter-exchange': exchange_name,
    #         'x-dead-letter-routing-key': queue_name
    #     })
    #     return queue
