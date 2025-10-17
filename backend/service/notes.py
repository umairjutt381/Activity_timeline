from bson import ObjectId
from fastapi import HTTPException
from starlette.responses import JSONResponse

from backend.utils.db_connection import activity_collection


def add_manual_notes(note,activity_id):
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


def delete_manual_notes(note_id):
    result = activity_collection.update_one(
        {"notes._id": note_id},
        {"$set": {"notes.$.isDeleted": True}}
    )
    if result.modified_count == 1:
        return JSONResponse(
            status_code=200,
            content={
                "message": "Notes deleted successfully",
                "note_id": note_id
            }
        )
    raise HTTPException(status_code=500, detail="Failed to delete note or note not found")


def update_manual_notes(note_id, note):
    update_data = note.model_dump()
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields provided to update")
    updated_fields = {f"notes.$.{k}": v for k, v in update_data.items()}
    result = activity_collection.update_one(
        {"notes._id": note_id},
        {"$set": updated_fields}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail=f"note with id {note_id} not found")
    if result.modified_count == 0:
        return JSONResponse(
            status_code=200,
            content={"message": "No changes detected", "note_id": note_id}
        )
    return JSONResponse(
        status_code=200,
        content={
            "message": "note updated successfully",
            "note_id": note_id,
            "updated_fields": updated_fields
        }
    )
