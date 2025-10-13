from fastapi import APIRouter
from backend.api.activity.schema.schemas import Activity, Note
from backend.service.manual_activity import create_manual_activity, get_manual_activity, get_activity_by_activity_id, \
    update_manual_activity, delete_manual_activity

router = APIRouter(prefix="/activity", tags=["activity"])

@router.post("/create_activity/{accountId}")
def create_activity(activity: Activity,accountId: str):
    return create_manual_activity(activity,accountId)


@router.get("/activities/{accountId}")
def get_activities(accountId: str):
    return get_manual_activity(accountId)
@router.get("/activity/{activity_id}")
def get_activity(activity_id: str):
    return get_activity_by_activity_id(activity_id)

@router.put("/activity/{activity_id}")
def update_activity(activity_id: str, update_data: Activity):
    return update_manual_activity(activity_id,update_data)

@router.delete("/activity/{activity_id}")
def delete_activity(activity_id: str):
    return delete_manual_activity(activity_id)


