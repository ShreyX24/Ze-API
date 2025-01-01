# app/database.py
import motor.motor_asyncio
from config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URL)
db = client[settings.DB_NAME]
user_collection = db[settings.USER_COLLECTION]