from functools import lru_cache

import asyncpg
from fastapi import Depends

from src.core.query import subscribe, unsubscribe
from src.core.settings import logger
from src.db.postgresdb import get_postgres
from src.storage.base import AsyncStorage
from src.storage.postgres import PSGR


class Subscribe:
    def __init__(self, storage: AsyncStorage):
        self.storage = storage

    async def unsubscribe(self, user_id: str):
        await self.storage.update(unsubscribe.format(user_id))
        logger.info('User with id = {0} has been unsubscribed')

    async def subscribe(self, user_id: str):
        await self.storage.update(subscribe.format(user_id))
        logger.info('User with id = {0} has been subscribed')


@lru_cache()
def get_subscribe_service(
    db: asyncpg.Connection = Depends(get_postgres),
) -> Subscribe:
    storage = PSGR(db)
    return Subscribe(storage)



