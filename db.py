from flask import Flask
from dotenv import load_dotenv
from flask_pymongo import pymongo
import os

load_dotenv()

CONNECTION_STRING = os.getenv("MONGO_URI")

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('flask_mongodb_atlas')
user_collection = pymongo.collection.Collection(db, 'user_collection')