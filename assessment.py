from pydantic import BaseModel
from typing import List, Dict, Optional, Any

print("!<----Verifying validity of Assessment Schema structure via pydantic---->!")

#### Assessment

class GenerateAssessmentNoteRequest(BaseModel):

    note_id: int

    mcq_count: int = 10

class AssessmentCreate(BaseModel):
    title: str
    note_id: int
    chapter_id: int
    lesson_id: int
    mcq_batch: int
    mcq_pool: List[Dict]
    answers_pool: List[Dict]

class AssessmentUpdate(BaseModel):
    print("!<----Assessment Updated---->!")
    title: Optional[str] = None
    chapter_id: Optional[int] = None
    lesson_id: Optional[int] = None
    mcq_batch: Optional[int] = None
    mcq_pool: Optional[Any] = None   # JSON field
    answers_pool: Optional[Any] = None  # JSON field
    published: Optional[bool] = None


class GoalRequest(BaseModel):
    goal: str

class Assessment(BaseModel):
    print("!<----Assessment Updated---->!")
    assessment_id : int
    title: str
    chapter_id : int
    lesson_id : int
    mcq_batch : int
    mcq_pool : str
    answers_pool : str
    published : bool
