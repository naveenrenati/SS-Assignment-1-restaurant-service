import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_mongo_uri() -> str:
    """
    Build the MongoDB URI.
    In Kubernetes, individual env vars (injected from Secret) are used.
    Locally, MONGO_URI from .env is used as fallback.
    """
    username = os.getenv("MONGO_USERNAME")
    password = os.getenv("MONGO_PASSWORD")
    host     = os.getenv("MONGO_HOST")
    port     = os.getenv("MONGO_PORT")
    database = os.getenv("MONGO_DATABASE")

    if all([username, password, host, port, database]):
        return f"mongodb://{username}:{password}@{host}:{port}/{database}?authSource=admin"

    return os.getenv("MONGO_URI", "mongodb://localhost:27017/foodappdb")


def get_database_name() -> str:
    return os.getenv("MONGO_DATABASE", "foodappdb")


client = MongoClient(get_mongo_uri())
db     = client[get_database_name()]
