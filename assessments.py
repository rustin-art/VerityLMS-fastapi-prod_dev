from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    Query
)

from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.assessment import (
    GenerateAssessmentNoteRequest,
    AssessmentCreate,
    AssessmentUpdate,
    GoalRequest
)

from ..services.assessment_service import (
    create_assessment,
    get_assessments,
    get_all_assessments,
    update_assessment,
    delete_assessment,
    generate_and_save_assessment,
    generate_assessment_from_notes
)

from ..services.note_lookup_service import get_note_by_id

router = APIRouter(
    prefix="/assessments",
    tags=["Assessments"]
    )

## API to create assessment
@router.post("/")
def create_assessment_api(
    assessment: AssessmentCreate,
    db: Session = Depends(get_db)
    ):

    print("<!---- Creating New Assessment ----!>")
    return create_assessment(
        db=db,
        assessment=assessment
    )

## API to search assessment
@router.get("/")
def get_assessments_api(
    assessment_id: Optional[int] = Query(None),
    title: Optional[str] = Query(None),
    chapter_id: Optional[int] = Query(None),
    lesson_id: Optional[int] = Query(None),
    published: Optional[bool] = Query(None),
    mcq_batch: Optional[int] = Query(None),
    db: Session = Depends(get_db)
    ):

    print("<!---- Fetching Assessment ----!>")
    return get_assessments(
        db=db,
        assessment_id=assessment_id,
        title=title,
        chapter_id=chapter_id,
        lesson_id=lesson_id,
        published=published,
        mcq_batch=mcq_batch
    )

## API to get all assessments
@router.get("/all")
def get_all_assessments_api(
    db: Session = Depends(get_db)
    ):

    print("<!---- Fetching All Assessments ----!>")
    return get_all_assessments(
        db=db
    )

## API to update assessment
@router.put("/{assessment_id}")
def update_assessment_api(
    assessment_id: int,
    assessment: AssessmentUpdate,
    db: Session = Depends(get_db)
    ):

    print("<!---- Fetching All Assessments ----!>")
    return update_assessment(
        db=db,
        assessment_id=assessment_id,
        assessment=assessment
    )

## API to Delete assessment
@router.delete("/{assessment_id}")
def delete_assessment_api(
    assessment_id: int,
    db: Session = Depends(get_db)
    ):

    print("!<----Deleting Assessment from Database---->!")
    return delete_assessment(
        db=db,
        assessment_id=assessment_id
    )

## API to generate assessment
@router.post("/generate")
def generate_assessment_api(
    goals: GoalRequest,
    db: Session = Depends(get_db)
    ):

    print("!<---- Agent is Generating Assessment ---->!")
    return generate_and_save_assessment(
        db=db,
        goal=goals.goal
    )


## API to generate Assessment from Note via pipeline
@router.post("/generate-from-note")
def generate_assessment(
    payload: GenerateAssessmentNoteRequest,
    db: Session = Depends(get_db)
):
    note = get_note_by_id(
        db,
        payload.note_id
    )

    return generate_assessment_from_notes(
        note.content,
        payload.mcq_count
    )