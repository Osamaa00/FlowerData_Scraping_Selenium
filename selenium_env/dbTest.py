from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://osamanadeem:bmw600bmw600@cluster0.8ke0m.mongodb.net/db_flowers?retryWrites=true&w=majority")
db = cluster['db_flowers']
collection = db['flowers']

collection.insert_one({ "name": "flower" })