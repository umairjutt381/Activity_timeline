from bson import ObjectId
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from datetime import datetime
from backend.utils.db_connection import activity_collection


def create_manual_activity(activity,accountId):
    activity_dict = activity.model_dump()
    activity_dict["accountId"] = accountId
    result = activity_collection.insert_one(activity_dict)
    if result.inserted_id:
        return JSONResponse(status_code=201, content={"message": "Activity created", "id": str(result.inserted_id)})
    raise HTTPException(status_code=500, detail="Failed to create activity due to some error")

def get_manual_activity(accountId):
    activities = []
    for activity in activity_collection.find({"accountId":accountId}):
        activity["_id"] = str(activity["_id"])
        activities.append(activity)
    return {"activities": activities}

def get_activity_by_activity_id(activity_id):
    obj_id = ObjectId(activity_id)
    activity = activity_collection.find_one({"_id": obj_id})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    activity["_id"] = str(activity["_id"])
    return activity

def update_manual_activity(activity_id,update_data):
    obj_id = ObjectId(activity_id)
    existing_activity = activity_collection.find_one({"_id": obj_id})
    if not existing_activity:
        raise HTTPException(status_code=404, detail="Activity not found")

    data_to_update = update_data.model_dump()
    if not data_to_update:
        raise HTTPException(status_code=400, detail="No fields provided for update")
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

def delete_manual_activity(activity_id):
    activity = activity_collection.find_one({"_id": ObjectId(activity_id)})
    if not activity:
        raise HTTPException(status_code=404, detail="Activity not found")
    deleted = activity_collection.delete_one({"_id": activity["_id"]})
    if deleted:
        return JSONResponse(status_code=200, content={"message": "Activity deleted successfully"})
    else:
        raise HTTPException(status_code=404, detail="Activity already not found")
