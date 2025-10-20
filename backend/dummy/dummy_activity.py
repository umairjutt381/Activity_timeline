import datetime
from bson import ObjectId
from faker import Faker
import random
from starlette.responses import JSONResponse
from backend.utils.db_connection import activity_collection

fake = Faker()

ACTIVITY_TYPES = ["meeting","notes","milestone"]
STATUSES = ["active","pending","completed"]
PRIORITIES = ["high","medium","low"]

def generate_activity_fake_data(number_of_activities: int,account_id:str):
    activity_fake_data = []
    for _ in range(number_of_activities):
        data = {
            "_id": ObjectId(),
            "accountId": account_id,
            "title": fake.word(),
            "activityDate":  fake.date_time_this_year(tzinfo=datetime.timezone.utc).isoformat()+"Z",
            "activityType": random.choice(ACTIVITY_TYPES),
            "loggedBy": fake.word(),
            "status": random.choice(STATUSES),
            "mention":[{"id": str(random.randint(1, 100)), "name": fake.word()}],
            "tasks":[{
                "id": fake.uuid4(),
                "taskName": fake.word(),
                "description": fake.sentence(),
                "assignedTo": [{"id": str(random.randint(1, 100)), "name": fake.word()}],
                "category": fake.word(),
                "status": fake.word(),
                "startDate": fake.date_time_this_year(tzinfo=datetime.timezone.utc).isoformat()+"Z",
                "dueDate": fake.date_time_this_year(tzinfo=datetime.timezone.utc).isoformat()+"Z",
                "createdBy":[{"id": str(random.randint(1, 100)), "name": fake.word()}],
                "priority": random.choice(PRIORITIES),
                "linkedOpportunity":[{"id": str(random.randint(1, 100)), "name": fake.word()}],
                "mention": [{"id": str(random.randint(1, 100)), "name": fake.word()}],
                "isDeleted": False
                 }],
            "notes":[{
                "id": fake.uuid4(),
                "text": fake.sentence(),
                "createdBy":[{"id": str(random.randint(1, 100)), "name": fake.word()}],
                "createdAt": fake.date_time_this_year(tzinfo=datetime.timezone.utc).isoformat()+"Z",
                "mention": [{"id": str(random.randint(1, 100)), "name": fake.word()}],
                "isDeleted": False
            }]
        }
        activity_fake_data.append(data)
    result = activity_collection.insert_many(activity_fake_data)
    return JSONResponse({"inserted_data": [str(obj_id) for obj_id in result.inserted_ids]})
