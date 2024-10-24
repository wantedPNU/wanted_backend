from motor.motor_asyncio import AsyncIOMotorClient
from config.config import Settings
from beanie import init_beanie
import models as models

from pymongo import MongoClient
from pymongo.database import Database


class MongoManager:
    def __init__(self):
        self.client: MongoClient = None
        self.db: Database = None
        self.db_logger = None
        self.db_name = "WANTED"

    async def initiate_database(self):
        self.client = AsyncIOMotorClient(Settings().DATABASE_URL)
        self.db=self.client.get_default_database()
        await init_beanie(
            self.db, document_models=models.__all__
        )
    
    