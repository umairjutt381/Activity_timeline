from fastapi import FastAPI
from backend.api.v1.manual_activity import  router as activity_router
from backend.api.v1.todo import  router as todos_router
from backend.api.v1.task import router as tasks_router
from backend.api.v1.notes import router as notes_router
from backend.api.v1.dummy_activity import router as dummy_activity_router
app = FastAPI()
app.include_router(activity_router)
app.include_router(todos_router)
app.include_router(tasks_router)
app.include_router(notes_router)
app.include_router(dummy_activity_router)