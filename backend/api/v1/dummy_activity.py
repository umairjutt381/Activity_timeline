from fastapi import APIRouter
from backend.dummy.dummy_activity import generate_activity_fake_data

router = APIRouter(prefix="/dummy", tags=["dummy"])

@router.get("/dummy_activity/{accountId}/{number_of_activities}")
async def dummy_activity(accountId:str ,number_of_activities: int):
    return generate_activity_fake_data(number_of_activities,account_id=accountId)
