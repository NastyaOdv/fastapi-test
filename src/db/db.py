import os

from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(os.getenv("DB_URL"))
database = client["speech_models"]
