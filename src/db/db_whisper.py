from pymongo.errors import PyMongoError

from src.db.db import database
from src.models.logger import logger
from src.models.whisper import Whisper


class CRUDWhisper:
    collection = database["whisper-audio-text"]

    def create(self, item: Whisper):
        try:
            result = self.collection.insert_one(item.to_dict())
            return result
        except PyMongoError as e:
            logger.error(f"Error inserting document into MongoDB: {e}")
            raise Exception("An error occurred while inserting the document into the database.")
