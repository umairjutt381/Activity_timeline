
from fastapi import APIRouter
from backend.api.activity.schema.schemas import Activity, Task, Note, Opportunity
from backend.service.manual_task import add_manual_task, delete_manual_task, update_manual_task, add_manual_opportunity

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/add task/{activity_id}")
def add_task(task: Task,activity_id: str):
    return add_manual_task(task,activity_id)

@router.delete("/delete task/{task_id}")
def delete_task( task_id: str):
    return delete_manual_task(task_id)

@router.patch("/update_task/{task_id}")
def update_task(task_id: str, task: Task):
    return update_manual_task(task_id,task)

@router.patch("/add opportunity/{task_id}")
def add_opportunity(opportunity: Opportunity,task_id: str):
    return add_manual_opportunity(opportunity,task_id)