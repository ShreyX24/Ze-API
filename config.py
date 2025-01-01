# app/config.py
from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    MONGODB_URL: str = os.getenv("MONGODB_URL")
    DB_NAME: str = "job-app"
    USER_COLLECTION: str = "user"

settings = Settings()