from fastapi import APIRouter

from backend.models.todo import TodoAccount
from backend.service.todo import get_manual_todo, status_mark_as_done

router = APIRouter(prefix="/todo",tags=["todo"])

@router.get("/get_todos/{account_id}",response_model=TodoAccount)
def get_todos(account_id: str):
   return get_manual_todo(account_id)

@router.patch("/mark_as_done/{task_id}",response_model=TodoAccount)
def mark_as_done(task_id: str):
    return status_mark_as_done(task_id)