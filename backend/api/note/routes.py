from fastapi import APIRouter
from backend.api.activity.schema.schemas import Note
from backend.service.manual_notes import add_manual_notes, delete_manual_notes, update_manual_notes


router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/add notes/{activity_id}")
def add_note(note: Note,activity_id: str):
    return add_manual_notes(note,activity_id)

@router.delete("/delete note/{note_id}")
def delete_notes( note_id: str):
    return delete_manual_notes(note_id)
@router.patch("/update_note/{note_id}")
def update_note(note_id: str, note: Note):
    return update_manual_notes(note_id,note)