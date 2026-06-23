from pydantic import BaseModel
from typing import List, Dict, Optional, Any

print("!<----Verifying validity of Homework Schema Structure via pydantic---->!")

#### HomeWork Model
class GenerateHomeworkNoteRequest(BaseModel):

    note_id: int

    question_count: int = 5  

class HomeworkCreate(BaseModel):
    title: str
    note_id: int
    chapter_id: int
    lesson_id: int
    homework_questions: List[Dict]

class HomeworkUpdate(BaseModel):
    title: Optional[str] = None
    chapter_id: Optional[int] = None
    lesson_id: Optional[int] = None
    homework_questions: Optional[Any] = None  # JSON field
    published: Optional[bool] = None


class GoalRequest(BaseModel):
    goal: str

class Homework(BaseModel):
    print("!<----Homework Updated---->!")
    homework_id : int
    title: str
    chapter_id : int
    lesson_id : int
    homework_questions: str
    published : bool