import uuid

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Literal, Union

class Note(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
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
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
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
    title: Optional[str] = None
    activityDate: Optional[datetime] = None
    loggedBy: Optional[str] = None
    status: Optional[str] = None

class Meeting(ActivityBase):
    activityType: Optional[Literal["meeting"]] = None
    internalAttendees: Optional[List[str]] = []
    externalAttendees: Optional[List[str]] = []
    notes: Optional[List[Note]] = []
    tasks: Optional[List[Task]] = []

class Notes(ActivityBase):
    activityType: Optional[Literal["notes"]] = None
    notes: Optional[List[Note]] = []
    tasks: Optional[List[Task]] = []

class Milestone(ActivityBase):
    activityType: Optional[Literal["milestone"]] = None
    milestoneType: Optional[str] = None
    notes: Optional[List[Note]] = []
    tasks: Optional[List[Task]] = []

Activity = Union[Meeting, Notes, Milestone]
