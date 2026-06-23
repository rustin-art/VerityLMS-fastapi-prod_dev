from pydantic import BaseModel
from typing import List, Dict, Optional, Any

print("!<----Verifying validity of Note Schema structure via pydantic---->!")

class GenerateDocumentNoteRequest(BaseModel):
    #This is for Extracted_document->LLM
    print("!<----Schema for Note Generation Pipeline---->!")
    document_id: int
    title: str
    chapter_id: int
    lesson_id: int
    goal: str


class NoteCreate(BaseModel):
    #Type Checking
    print("!<----Creating Notes---->!")
    title: str
    chapter_id : int
    lesson_id : int
    content: str

class NoteUpdate(BaseModel):
    #Type Checking
    print("!<----Updating Notes---->!")
    title: Optional[str] = None
    chapter_id: Optional[int] = None
    lesson_id: Optional[int] = None
    content: Optional[str] = None
    published: Optional[bool] = None

class GoalRequest(BaseModel):
    goal: str

class Note(BaseModel):
    notes_id: int
    title: str
    chapter_id : int
    lesson_id : int
    content: str
    published: bool
