import asyncpg
import psycopg2
import psycopg2.extras

from src.core.settings import logger
from src.storage.base import AsyncStorage
from src.core.settings import PostgresSettings


class PSGR(AsyncStorage):
    def __init__(self, db: asyncpg.Connection):
        self.db = db

    async def get(self, query: str):
        data = await self.db.fetch(query)
        return data

    async def insert_many(self, query: str, values: list[str]):
        await self.db.executemany(query, values)

    async def update(self, query: str):
        await self.db.execute(query)


class Postgres:
    def __init__(self):
        self.database = PostgresSettings()
        self.connection = self.postgres_connection()

    def postgres_connection(self):
        settings = {'dbname': self.database.database,
                    'user': self.database.user,
                    'password': self.database.password,
                    'host': self.database.host,
                    'port': int(self.database.port)}
        return psycopg2.connect(**settings)

    def get_data(self, query):
        with self.connection.cursor() as curs:
            curs.execute(query)
            try:
                records = curs.fetchall()
                columns = [desc[0] for desc in curs.description]
                params = [{key: value for key, value in zip(columns, row)} for row in records]
                return records, params
            except psycopg2.ProgrammingError:
                logger.info('No result')
                return None

    def insert_update(self, query):
        with self.connection.cursor() as curs:
            curs.execute(query)
        self.connection.commit()

    def insert_many(self, query, data):
        with self.connection.cursor() as curs:
            psycopg2.extras.execute_values(curs, query, data)
        self.connection.commit()


