from fastapi import HTTPException

from backend.models.todo import TodoAccount
from backend.utils.db_connection import activity_collection


def get_manual_todo(account_id):
    pipeline = [
        {"$match": {"accountId": account_id}},
        {"$unwind": "$tasks"},
        {"$match": {"tasks.isDeleted": False}},
        {"$group": {
            "_id": "$accountId",
            "tasks": {"$push": "$tasks"}
        }},
        {"$project": {
            "_id": 0,
            "accountId": "$_id",
            "tasks": 1
        }}
    ]
    account = list(activity_collection.aggregate(pipeline))
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return TodoAccount(**account[0])

def status_mark_as_done(task_id):
    result = activity_collection.update_one({"tasks._id": task_id}, {"$set": {"tasks.$.status": "completed"}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    updated = activity_collection.find_one({"tasks._id": task_id}, {"tasks.$": 1, "accountId": 1, "_id": 0})
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return TodoAccount(**updated)