from fastapi import APIRouter,Query

from typing import Optional, List
from backend.models.manual_activity import Activity
from backend.service.manual_activity import create_manual_activity, get_manual_activity, get_activity_by_activity_id, \
    update_manual_activity, delete_manual_activity

router = APIRouter(prefix="/activity", tags=["activity"])

@router.post("/create_activity/{accountId}")
def create_activity(activity: Activity,accountId:str):
    return create_manual_activity(activity,accountId)


@router.get("/activities/{accountId}")
def get_activities(
        accountId:str,
        activityType: Optional[str] = Query(None,description="The type of activity to get"),
        loggedBy: Optional[str] = Query(None),
        opportunityId: Optional[int] = Query(None),
        opportunityName: Optional[str] = Query(None),
        days: Optional[int] = Query(None),
):
    return get_manual_activity(accountId,activityType,loggedBy,opportunityId,opportunityName,days)
@router.get("/activity/{activity_id}")
def get_activity(activity_id: str):
    return get_activity_by_activity_id(activity_id)

@router.patch("/activity/{activity_id}")
def update_activity(activity_id: str, update_data: Activity):
    return update_manual_activity(activity_id,update_data)

@router.delete("/activity/{activity_id}")
def delete_activity(activity_id: str):
    return delete_manual_activity(activity_id)


