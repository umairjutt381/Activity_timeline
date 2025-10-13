from fastapi import FastAPI
from backend.api.activity.routes import  router as activity_router
from backend.api.todo.routes import router as todos_router
from backend.api.task.routes import router as tasks_router
from backend.api.note.routes import router as notes_router
app = FastAPI()
app.include_router(activity_router)
app.include_router(todos_router)
app.include_router(tasks_router)
app.include_router(notes_router)