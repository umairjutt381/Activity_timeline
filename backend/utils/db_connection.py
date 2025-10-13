from pymongo import MongoClient

client = MongoClient("mongodb://admin:StrongPassword123@127.0.0.1:27017/admin")
db = client["ActivityTimeline"]
activity_collection = db["activity_timeline"]