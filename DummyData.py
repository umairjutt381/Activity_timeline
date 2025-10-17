import datetime
import json

from bson import ObjectId
from faker import Faker
import random
from starlette.responses import JSONResponse
from backend.utils.db_connection import activity_collection

fake = Faker()

ACTIVITY_TYPES = ["meeting","notes","milestone"]
STATUSES = ["active","pending","completed"]
PRIORITIES = ["high","medium","low"]

def convert_objectId_to_str(obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def generate_activity_fake_data(number_of_activities):
    activity_fake_data = []
    for _ in range(number_of_activities):
        data = {
            "_id": ObjectId(),
            "title": fake.word(),
            "activityDate":  fake.date_time_this_year(tzinfo=datetime.timezone.utc).isoformat()+"Z",
            "activityType": random.choice(ACTIVITY_TYPES),
            "loggedBy": fake.word(),
            "status": random.choice(STATUSES),
            "tasks":[{
                "id": fake.uuid4(),
                "taskName": fake.word(),
                "description": fake.sentence(),
                "assignedTo": fake.word(),
                "category": fake.word(),
                "status": fake.word(),
                "startDate": fake.date_time_this_year(tzinfo=datetime.timezone.utc).isoformat()+"Z",
                "dueDate": fake.date_time_this_year(tzinfo=datetime.timezone.utc).isoformat()+"Z",
                "createdBy":[{"id": random.randint(1, 100), "name": fake.word()}],
                "priority": random.choice(PRIORITIES),
                "linkedOpportunity":[{"id": random.randint(1, 100), "name": fake.word()}],
                "isDeleted": False
                 }],
            "notes":[{
                "id": fake.uuid4(),
                "text": fake.sentence(),
                "createdBy":[{"id": random.randint(1, 100), "name": fake.word()}],
                "createdAt": fake.date_time_this_year(tzinfo=datetime.timezone.utc).isoformat()+"Z",
                "isDeleted": False
            }]
        }
        activity_fake_data.append(data)
    json_string = json.dumps(activity_fake_data,indent=4,default=convert_objectId_to_str)
    print(json_string)
    result = activity_collection.insert_many(activity_fake_data)
    print({"inserted_data": [str(obj_id) for obj_id in result.inserted_ids]})

number_of_activities = int(input("enter number of activities: "))
generate_activity_fake_data(number_of_activities)