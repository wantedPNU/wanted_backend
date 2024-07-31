from motor.motor_asyncio import AsyncIOMotorClient
from config.config import Settings
from beanie import init_beanie
import models as models

async def initiate_database():
    client = AsyncIOMotorClient(Settings().DATABASE_URL)
    await init_beanie(
        database=client.get_default_database(), document_models=models.__all__
    )
