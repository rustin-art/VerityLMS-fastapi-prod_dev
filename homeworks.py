from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    Query
)

from sqlalchemy.orm import Session

from ..database import get_db

from ..schemas.homework import (
    GenerateHomeworkNoteRequest,
    HomeworkCreate,
    HomeworkUpdate,
    GoalRequest
)

from ..services.homework_service import (
    create_homework,
    get_homeworks,
    get_all_homeworks,
    update_homework,
    delete_homework,
    generate_and_save_homework,
    generate_homework_from_notes
)

from ..services.note_lookup_service import get_note_by_id

router = APIRouter(
    prefix="/homeworks",
    tags=["Homeworks"]
)


# -----------------------------
# Create Homework
# -----------------------------
@router.post("/")
def create(
    homework: HomeworkCreate,
    db: Session = Depends(get_db)
):
    return create_homework(
        db,
        homework
    )


# -----------------------------
# Get Homework(s)
# -----------------------------
@router.get("/")
def get(
    homework_id: Optional[int] = Query(None),
    title: Optional[str] = Query(None),
    chapter_id: Optional[int] = Query(None),
    lesson_id: Optional[int] = Query(None),
    published: Optional[bool] = Query(None),
    db: Session = Depends(get_db)
):
    return get_homeworks(
        db=db,
        homework_id=homework_id,
        title=title,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
        published=published
    )


# -----------------------------
# Get All Homework
# -----------------------------
@router.get("/all")
def get_all(
    db: Session = Depends(get_db)
):
    return get_all_homeworks(
        db
    )


# -----------------------------
# Update Homework
# -----------------------------
@router.put("/{homework_id}")
def update(
    homework_id: int,
    homework: HomeworkUpdate,
    db: Session = Depends(get_db)
):
    return update_homework(
        db,
        homework_id,
        homework
    )


# -----------------------------
# Delete Homework
# -----------------------------
@router.delete("/{homework_id}")
def delete(
    homework_id: int,
    db: Session = Depends(get_db)
):
    return delete_homework(
        db,
        homework_id
    )


# -----------------------------
# Generate Homework
# -----------------------------
@router.post("/generate")
def generate(
    goals: GoalRequest,
    db: Session = Depends(get_db)
):
    return generate_and_save_homework(
        db=db,
        goal=goals.goal
    )

# -----------------------------
# Generate Homework from Notes
# -----------------------------

@router.post("/generate-from-note")
def generate_homework(
    payload: GenerateHomeworkNoteRequest,
    db: Session = Depends(get_db)
):
    note = get_note_by_id(
        db,
        payload.note_id
    )

    return generate_homework_from_notes(
        note.content,
        payload.question_count
    )