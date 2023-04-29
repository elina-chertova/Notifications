import asyncio
import json
import time

from aio_pika import DeliveryMode, Message, connect
from aio_pika.abc import AbstractIncomingMessage

from generator.models.event import Event
from src.worker.broker.base import BaseQueue
from src.core.settings import Settings, logger
from src.worker.source.email.send_email import Email


class RabbitMQ(BaseQueue):
    def __init__(self):
        self.settings = Settings()
        self.host = self.settings.rabbit_host
        self.login = self.settings.rabbit_login
        self.password = self.settings.rabbit_pswd
        self.email_ = Email()

    async def declare_dlq(self, dlq_name, exchange_name):
        connection = await connect("amqp://{0}:{1}@{2}/".format(
            self.login, self.password, self.host
        ))
        channel = await connection.channel()
        exchange = await channel.declare_exchange(
            name=exchange_name, type='direct', durable=True
        )
        dlq = await channel.declare_queue(dlq_name, durable=True, dead_letter_exchange=exchange)
        return connection, channel, exchange, dlq

    async def declare(self, queue_name, exchange_name, exchange_type, routing_key):
        connection = await connect(f"amqp://{self.login}:{self.password}@{self.host}/")
        channel = await connection.channel()
        exchange = await channel.declare_exchange(
            name=exchange_name, type=exchange_type, durable=True
        )
        queue = await channel.declare_queue(queue_name, durable=True, arguments={
            'x-dead-letter-exchange': 'dlx_exchange',
            'x-dead-letter-routing-key': 'dlx_routing_key'
        })
        await queue.bind(exchange, routing_key)

        return connection, channel, exchange, queue

    async def produce(self,
                      msg,
                      queue_name: str,
                      exchange_name: str,
                      routing_key: str,
                      headers: str = None,
                      exchange_type: str = 'direct'):

        _, _, exchange, queue = await self.declare(queue_name, exchange_name, exchange_type, routing_key)
        message = Message(headers=headers or {},
                          body=bytes(msg, 'utf-8'),
                          delivery_mode=DeliveryMode.PERSISTENT)
        message.headers['dead_letter_routing_key'] = f"{queue_name}-dlq"
        await exchange.publish(message, routing_key)
        logger.info(
            'Exchange name: {0}. Queue name: {1}. Sent message: {2}'.format(
                exchange_name, queue_name, message)
        )
        time.sleep(0.01)

    async def choose_ntf_type(self, message: dict):
        if message['destination'] == 'Email':
            try:
                self.email_.send(email=message['email'], subject=message['subject'], template=message['template'])
                self.email_.commit(message)
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

        async with connection:
            await channel.set_qos(prefetch_count=1)
            print(" [*] Waiting for logs. To exit press CTRL+C")
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    try:
                        event = Event(**json.loads(message.body)).dict()
                        await self.choose_ntf_type(event)
                        print(event)
                        await message.ack()
                    except Exception as e:
                        print('Error processing message:', e)
                        await message.reject(requeue=False)
            if channel._unacked:
                await channel._unacked.reject_all(requeue=False)
