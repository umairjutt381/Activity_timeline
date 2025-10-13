from bson import ObjectId
from fastapi import APIRouter
from backend.api.activity.schema.schemas import Activity, Task, Note, Opportunity
from backend.utils.db_connection import activity_collection
from fastapi import HTTPException
from fastapi.responses import JSONResponse



router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/add task/{activity_id}")
def add_task(task: Task,activity_id: str):
    obj_id = ObjectId(activity_id)
    activity = activity_collection.find_one({"_id": obj_id})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    task_dict = task.model_dump()
    result = activity_collection.update_one(
        {"_id": obj_id},
        {"$push": {"tasks": task_dict}}
    )
    if result.modified_count == 1:
        return JSONResponse(status_code=201, content={"message": "task added"})
    raise HTTPException(status_code=500, detail="failed to add task")

@router.delete("/delete task/{task_id}")
def delete_task( task_id: str):
    result = activity_collection.update_one(
        {"tasks._id": task_id},
        {"$set": {"tasks.$.isDeleted": True}}
    )
    if result.modified_count == 1:
        return JSONResponse(
            status_code=200,
            content={
                "message": "Task deleted successfully",
                "task_id": task_id
            }
        )
    raise HTTPException(status_code=500, detail="Failed to delete task or task not found")

@router.patch("/update_task/{task_id}")
def update_task(task_id: str, task: Task):
    update_data = task.dict(exclude_unset=True, by_alias=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided to update")
    updated_fields = {f"tasks.$.{k}": v for k, v in update_data.items()}
    result = activity_collection.update_one(
        {"tasks._id": task_id},
        {"$set": updated_fields}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    if result.modified_count == 0:
        return JSONResponse(
            status_code=200,
            content={"message": "No changes detected", "task_id": task_id}
        )
    return JSONResponse(
        status_code=200,
        content={
            "message": "Task updated successfully",
            "task_id": task_id,
            "updated_fields": updated_fields
        }
    )

@router.patch("/add opportunity/{task_id}")
def add_opportunity(opportunity: Opportunity,task_id: str):
    update_data = opportunity.model_dump()
    update_task = activity_collection.update_one({"tasks._id":task_id}, {"$set": {"linkedOpportunity":update_data}})
    if update_task.modified_count == 0:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return {"message": "Opportunity updated successfully"}