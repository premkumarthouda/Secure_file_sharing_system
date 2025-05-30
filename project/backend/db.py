from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os


client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["secure_file_sharing"]

user_collection = db["users"]
file_collection = db["files"]