# app/db/connection.py

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os

# -----------------------------------------------------------
# ✅ Global variable to hold the MongoDB client
# -----------------------------------------------------------
mongo_client = None
db = None


# -----------------------------------------------------------
# ✅ MongoDB Connection
# -----------------------------------------------------------
def connect_to_mongo():
    """
    Connect to MongoDB (local or Atlas) and initialize global db instance.
    """
    global mongo_client, db

    # Environment variable or fallback for development
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    DB_NAME = os.getenv("MONGO_DB_NAME", "langchatbot_db")

    try:
        mongo_client = MongoClient(MONGO_URI)
        # Ping the server
        mongo_client.admin.command("ping")
        db = mongo_client[DB_NAME]
        print(f"✅ Connected to MongoDB → {DB_NAME}")

    except ConnectionFailure as e:
        print("❌ MongoDB connection failed:", e)
        raise e


# -----------------------------------------------------------
# ✅ Helper to get collection
# -----------------------------------------------------------
def get_collection(collection_name: str):
    """
    Return a MongoDB collection by name.
    Example: users = get_collection("users")
    """
    if db is None:
        raise Exception("Database not connected. Call connect_to_mongo() first.")
    return db[collection_name]
