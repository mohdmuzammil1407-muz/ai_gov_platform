import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / ".env")

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "ai_gov")

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

users_collection = db["users"]
citizens_collection = db["citizens"]
complaints_collection = db["complaints"]
settings_collection = db["system_settings"]
