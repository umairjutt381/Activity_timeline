from fastapi import APIRouter, HTTPException
from backend.api.todo.schema.schemas import TodoAccount
from backend.utils.db_connection import activity_collection

router = APIRouter(prefix="/todo",tags=["todo"])

@router.get("/get_todos/{account_id}",response_model=TodoAccount)
def get_todos(account_id: str):
    pipeline = [
        {
            "$match": {"accountId": account_id}
        },
        {
            "$project": {
                "_id": 0,
                "accountId": 1,
                "tasks": {
                    "$filter": {
                        "input": "$tasks",
                        "as": "task",
                        "cond": {"$eq": ["$$task.isDeleted", False]}
                    }
                }
            }
        }
    ]
    account = list(activity_collection.aggregate(pipeline))
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return TodoAccount(**account[0])

@router.patch("/mark_as_done/{task_id}",response_model=TodoAccount)
def mark_as_done(task_id: str):
    result = activity_collection.update_one({"tasks._id": task_id}, {"$set":{"tasks.$.status": "completed"}})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    updated = activity_collection.find_one({"tasks._id": task_id},{"tasks.$": 1,"accountId": 1, "_id": 0})
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    return TodoAccount(**updated)