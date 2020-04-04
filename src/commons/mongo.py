from typing import Optional

from flask_pymongo.wrappers import (
    Collection,
    Database,
)


class MongoRepository:
    __slots__ = ('_mongo_conn', '_database', '_collection')

    def __init__(self, mongo_connection):
        self._mongo_conn = mongo_connection
        self._database: Database = None
        self._collection: Collection = None
        self.reconnect()

    def get_database_name(self) -> Optional[str]:
        return self._mongo_conn.db.name

    @classmethod
    def get_collection_name(cls) -> str:
        raise NotImplementedError()

    def reconnect(self):
        self._database = self._mongo_conn.db
        self._collection = self._database.get_collection(self.get_collection_name())

    def drop_collection(self):
        return self._collection.drop()

    @property
    def collection(self) -> Collection:
        return self._collection

    @collection.setter
    def collection(self, value):
        raise ValueError("Cannot set connection")

    def create_indexes(self):
        pass

    def close_connection(self):
        self._mongo_conn._db_client.close()
