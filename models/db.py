from decouple import config
from pymongo import MongoClient


MONGO_USERNAME = config("MONGO_USERNAME")
MONGO_PASSWORD = config("MONGO_PASSWORD")
MONGO_HOST = config("MONGO_HOST")
MONGO_PORT = config("MONGO_PORT", cast=int)
MONGO_DB = config("MONGO_DB")

client = MongoClient(config("MONGO_URL"))
db = client[MONGO_DB]
string_collection = db['text']
