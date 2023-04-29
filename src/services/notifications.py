from functools import lru_cache

import asyncpg
from fastapi import Depends

from src.core.settings import logger
from src.db.postgresdb import get_postgres
from src.storage.base import AsyncStorage
from src.storage.postgres import PSGR
import src.core.query as sql_query
from src.worker.source.email.send_email import Email
from generator.models.event import Event
import uuid
import datetime
from src.worker.broker.rabbitmq import RabbitMQ
from src.core.settings import rabbit_settings


class Notifier:
    def __init__(self, storage: AsyncStorage):
        self.storage = storage
        self.email = Email()
        self.broker = RabbitMQ()

    async def get_users(self, user_id: str = None):
        if user_id is not None:
            users = await self.storage.get(sql_query.users.format(user_id))
        else:
            users = await self.storage.get(sql_query.users_A)
        return users

    async def send(self, user_id: str, subject: str,
                   title: str, text: str, content: str,
                   destination: str, headers: str):
        ntf_id = uuid.uuid4()
        msg_type = 'Service'
        users = await self.get_users(user_id=user_id)

        for user in users:
            row = [(user['id'], user['email'], user['first_name'], user['last_name'], str(ntf_id), destination,
                    'site', subject, title, text, content, 'high', datetime.datetime.now(), msg_type, 'pending'), ]
            await self.storage.insert_many(sql_query.insert_us_ntf_as, row)
            user_ = user['first_name'] + ' ' + user['last_name']
            params = {
                'user': user_,
                'title': title,
                'text': text,
                'content': content
            }
            if destination == 'Email':
                template = self.email.render_template(source=msg_type, params=params, msg_type='')
                event = Event(user_id=user['id'],
                              ntf_id=str(ntf_id),
                              msg_type=msg_type,
                              email=user['email'],
                              subject=subject,
                              destination=destination,
                              template=template)
                await self.broker.produce(msg=event.json(),
                                          queue_name=rabbit_settings.queue_email,
                                          exchange_name=rabbit_settings.exchange,
                                          headers=headers,
                                          routing_key='email.service')
                logger.info('Added service event to rabbitmq')


@lru_cache()
def get_notifier_service(
    db: asyncpg.Connection = Depends(get_postgres),
) -> Notifier:
    storage = PSGR(db)
    return Notifier(storage)


