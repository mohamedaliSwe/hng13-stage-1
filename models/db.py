from decouple import config
from pymongo import MongoClient


client = MongoClient(config("MONGO_URL"))
db = client.text_analyzer_db
string_collection = db['text']
