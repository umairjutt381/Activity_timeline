
from pydantic import BaseModel, Field
from typing import Optional, List

from backend.models.manual_activity import User

class TodoTask(BaseModel):
    id: Optional[str] = Field(None, alias="_id")
    assignedTo: Optional[User] = None
    status: Optional[str] = None
    startDate: Optional[str] = None
    dueDate: Optional[str] = None
    createdBy: Optional[User] = None
    priority: Optional[str] = None
    isDeleted: Optional[bool] = False

class TodoAccount(BaseModel):
    accountId: str
    tasks: List[TodoTask] = []