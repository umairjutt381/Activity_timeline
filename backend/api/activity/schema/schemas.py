from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Literal, Union

class Note(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    text: Optional[str] = None
    createdBy: Optional[str] = None
    createdAt: Optional[datetime] = None
    isDeleted: Optional[bool] = False


class Opportunity(BaseModel):
    opportunityId: str
    as_of_opportunity : str

class User(BaseModel):
    id: str
    name: str

class Task(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    taskName: Optional[str] = None
    description: Optional[str] = None
    assignedTo: Optional[User] = None
    category: Optional[str] = None
    status: Optional[str] = None
    startDate: Optional[str] = None
    dueDate: Optional[str] = None
    createdBy: Optional[User] = None
    priority: Optional[str] = None
    linkedOpportunity: Optional[Opportunity] = None
    isDeleted: Optional[bool] = False

class ActivityBase(BaseModel):
    accountId: Optional[str] = None
    title: Optional[str] = None
    activityDate: Optional[datetime] = None
    loggedBy: Optional[str] = None
    status: Optional[str] = None

class Meeting(ActivityBase):
    activityType: Optional[Literal["meeting"]] = None
    internalAttendees: Optional[List[str]] = None
    externalAttendees: Optional[List[str]] = None
    notes: Optional[List[Note]] = None
    tasks: Optional[List[Task]] = None

class Notes(ActivityBase):
    activityType: Optional[Literal["notes"]] = None
    notes: Optional[List[Note]] = None
    tasks: Optional[List[Task]] = None

class Milestone(ActivityBase):
    activityType: Optional[Literal["milestone"]] = None
    milestoneType: Optional[str] = None
    notes: Optional[List[Note]] = None
    tasks: Optional[List[Task]] = None

Activity = Union[Meeting, Notes, Milestone]
