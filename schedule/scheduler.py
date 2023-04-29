import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

import src.core.query as sql_query
from generator.ntf_prep import UserNtfPrep
from generator.tasks.adm_pan import AdminPanel
from generator.tasks.tasks import Tasks
from schedule.triggers import tasks_trigger
from src.core.settings import logger, rabbit_settings
from src.storage.postgres import Postgres
from src.worker.broker.rabbitmq import RabbitMQ


class Scheduler(Tasks):
    def __init__(self, trigger: dict):
        super().__init__()
        self.db = Postgres()
        self.broker = RabbitMQ()
        self.prepare = UserNtfPrep()
        self.trigger = trigger
        self.adm = AdminPanel()

    async def choose_ntf_type(self,
                              msg_type: str) -> list:
        events_ = None
        if msg_type == 'best_movies':
            self.prepare.run(query=sql_query.gen.format('Auto', msg_type))
            events_ = await self.best_movies_task()
        elif msg_type == 'Admin':
            events_ = await self.adm.send_event()
        else:
            logger.info('Unexpected message type in scheduler')
        return events_

    async def send_notification(self,
                                msg_type: str,
                                queue_name: str,
                                exchange_name: str,
                                routing_key: str) -> None:

        events = await self.choose_ntf_type(msg_type=msg_type)
        if events is None:
            logger.info("No one notification with {0} type doesn't exist.".format(msg_type))
            return None
        for event in events:
            await self.broker.produce(msg=event.json(),
                                      queue_name=queue_name,
                                      exchange_name=exchange_name,
                                      routing_key=routing_key)

    def __call__(self):
        scheduler = AsyncIOScheduler()
        scheduler.start()

        scheduler.add_job(
            self.send_notification,
            trigger=self.trigger[rabbit_settings.routing_key_email.format('auto', 'best_movies')],
            args=["best_movies", rabbit_settings.queue_email, rabbit_settings.exchange,
                  rabbit_settings.routing_key_email.format('auto', 'best_movies')],
            name="best_movies",
        )
        scheduler.add_job(
            self.send_notification,
            trigger=self.trigger[rabbit_settings.routing_key_email.format('admin', 'any')],
            args=["Admin", rabbit_settings.queue_email, rabbit_settings.exchange,
                  rabbit_settings.routing_key_email.format('admin', 'any')],
            name="Admin",
        )
        try:
            asyncio.get_event_loop().run_forever()
        except (KeyboardInterrupt, SystemExit):
            pass


if __name__ == "__main__":
    schedule = Scheduler(trigger=tasks_trigger)
    schedule()
