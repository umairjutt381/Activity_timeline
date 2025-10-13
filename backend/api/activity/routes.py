from bson import ObjectId
from fastapi import APIRouter
from backend.api.activity.schema.schemas import Activity, Task, Note, Opportunity
from backend.utils.db_connection import activity_collection
from datetime import datetime
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/activity", tags=["activity"])

@router.post("/create_activity/{accountId}")
def create_activity(activity: Activity,accountId: str):
    activity_dict = activity.dict(by_alias=True)
    activity_dict["accountId"] = accountId
    result = activity_collection.insert_one(activity_dict)
    if result.inserted_id:
        return JSONResponse(status_code=201, content={"message": "Activity created", "id": str(result.inserted_id)})
    raise HTTPException(status_code=500, detail="Failed to create activity due to some error")

@router.get("/activities")
def get_activities():
    activities = []
    for activity in activity_collection.find():
        activity["_id"] = str(activity["_id"])
        activities.append(activity)
    return {"activities": activities}

@router.get("/activity/{activity_id}")
def get_activity(activity_id: str):
    obj_id = ObjectId(activity_id)
    activity = activity_collection.find_one({"_id": obj_id})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity["_id"] = str(activity["_id"])
    return activity

@router.put("/activity/{activity_id}")
def update_activity(activity_id: str, update_data: Activity):
    obj_id = ObjectId(activity_id)
    existing_activity = activity_collection.find_one({"_id": obj_id})
    if not existing_activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    data_to_update = update_data.dict(exclude_unset=True, by_alias=True)
    if not data_to_update:
        raise HTTPException(status_code=400, detail="No fields provided for update")

    data_to_update["updatedAt"] = datetime.utcnow()

    result = activity_collection.update_one(
        {"_id": obj_id},
        {"$set": data_to_update}
    )

    if result.modified_count == 1:
        updated = activity_collection.find_one({"_id": obj_id})
        updated["_id"] = str(updated["_id"])
        json_ready_activity = jsonable_encoder(updated)
        return JSONResponse(status_code=200, content={
            "message": "Activity updated successfully",
            "activity": json_ready_activity
        })
    else:
        return JSONResponse(status_code=200, content={"message": "No changes made"})

@router.delete("/activity/{activity_id}")
def delete_activity(activity_id: str):
    activity = activity_collection.find_one({"_id": ObjectId(activity_id)})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    deleted = activity_collection.delete_one({"_id": activity["_id"]})
    if deleted:
        return JSONResponse(status_code=200, content={"message": "Activity deleted successfully"})
    else:
        raise HTTPException(status_code=404, detail="Activity already not found")


@router.post("/add notes/{activity_id}")
def add_note(note: Note,activity_id: str):
    obj_id = ObjectId(activity_id)
    activity = activity_collection.find_one({"_id": obj_id})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    note_dict = note.model_dump()
    result = activity_collection.update_one(
        {"_id": obj_id},
        {"$push": {"notes": note_dict}}
    )
    if result.modified_count == 1:
        return JSONResponse(status_code=201, content={"message": "note added"})
    raise HTTPException(status_code=500, detail="failed to add task")

@router.delete("/delete note/{note_id}")
def delete_notes( note_id: str):
    result = activity_collection.update_one(
        {"notes._id": note_id},
        {"$set": {"notes.$.isDeleted": True}}
    )
    if result.modified_count == 1:
        return JSONResponse(
            status_code=200,
            content={
                "message": "Task deleted successfully",
                "note_id": note_id
            }
        )
    raise HTTPException(status_code=500, detail="Failed to delete task or task not found")


