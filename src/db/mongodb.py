import uuid

from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, BaseSettings


class BookmarkModel(BaseModel):
    movie_id: uuid.UUID


class MongoDB(BaseSettings):
    mongodb_host: str = "localhost"
    mongodb_port: str = "27017"
    db_collection: dict = {'Bookmarks': 'BookmarksCollection'}
    database: str = 'Bookmarks'


class UGC:
    def __init__(self):
        self.config = MongoDB()

    @staticmethod
    async def connection(database):
        return AsyncIOMotorClient(host=database.mongodb_host,
                                  port=int(database.mongodb_port),
                                  directConnection=True)

    async def collection(self, database: str):
        """
        Get MongoDB collection.
        :param database: database name
        :return:
        """
        connection = await self.connection(self.config)
        db = connection.get_database(database)
        collection = db.get_collection(self.config.db_collection[database])
        return collection

    async def get(self, database: str, params: dict, filter_=None) -> list[dict]:
        """
        Get documents.
        :param database: database name
        :param params: params for request
        :param filter_: filter for request
        :return:
        """
        if filter_ is None:
            filter_ = {}
        collection = await self.collection(database)
        cursor = collection.find(params, filter_)
        documents = [document for document in await cursor.to_list(length=100)]
        return documents

    async def get_bookmarks(self, user_id):
        """
        Get all user's bookmarks.
        :param user_id:
        :return:
        """
        params = {'user_id': user_id}
        filter_ = {"_id": 0, 'user_id': 0}
        all_bookmarks = await self.get(database=self.config.database, params=params, filter_=filter_)
        result = [BookmarkModel(movie_id=item['movie_id']) for item in all_bookmarks]
        return result

