import os

from dotenv import load_dotenv

load_dotenv()

class MongoDBConfig:
  USERNAME = os.environ.get("MONGO_USERNAME") or ""
  PASSWORD = os.environ.get("MONGO_PASSWORD") or ""
  HOST = os.environ.get("MONGO_HOST") or "localhost"
  PORT = os.environ.get("MONGO_PORT") or "27017"
  DATABASE = os.environ.get("MONGO_DBS") or ""
  USER_COLLECTION = os.environ.get("MONGO_USER_COLLECTION") or ""
  SPENDING_COLLECTION = os.environ.get("MONGO_SPENDING_COLLECTION") or ""
  COMMENT_COLLECTION = os.environ.get("MONGO_COMMENT_COLLECTION") or ""
  ASSETS_COLLECTION = os.environ.get("MONGO_ASSETS_COLLECTION") or ""