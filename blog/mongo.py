from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['blogger']
collection = db['blogg']