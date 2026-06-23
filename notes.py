from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    Query
)

from sqlalchemy.orm import Session

from ..database import get_db

from ..schemas.note import (
    NoteCreate,
    NoteUpdate,
    GoalRequest
)

from ..services.note_service import (
    create_note,
    get_notes,
    get_all_notes,
    regenerate_note,
    update_note,
    delete_note,
    generate_and_save_notes
)

router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
    )


## API to create Note
@router.post("/")
def create_note_api(
    note: NoteCreate,
    db: Session = Depends(get_db)
    ):

    print("<!---- Creating New Note ----!>")
    return create_note(
        db=db,
        note=note
    )

## API to get single note
@router.get("/")
def get_notes_api(
    notes_id: Optional[int] = Query(None),
    title: Optional[str] = Query(None),
    chapter_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
    ):

    print("<!---- Fetching Single Note ----!>")
    return get_notes(
        db=db,
        notes_id=notes_id,
        title=title,
        chapter_id=chapter_id
    )


## API to get all Notes
@router.get("/all")
def get_all_notes_api(
    db: Session = Depends(get_db)
    ):

    print("<!---- Fetching All Notes ----!>")
    return get_all_notes(
        db=db
    )


## API to update Notes based on id
@router.put("/{notes_id}")
def update_note_api(
    notes_id: int,
    note: NoteUpdate,
    db: Session = Depends(get_db)
    ):

    print("<!---- Updating Note ----!>")
    return update_note(
        db=db,
        notes_id=notes_id,
        note=note
    )

## API to delete Notes based on id
@router.delete("/{notes_id}")
def delete_note_api(
    notes_id: int,
    db: Session = Depends(get_db)
    ):

    print("!<----Deleting Note from Database---->!")
    return delete_note(
        db=db,
        notes_id=notes_id
    )

## API to Generate Note from LLM
@router.post("/generate")
def generate_notes_api(
    goals: GoalRequest,
    db: Session = Depends(get_db)
    ):
    
    print("!<---- Agent is Generating Notes ---->!")
    return generate_and_save_notes(
        db=db,
        goal=goals.goal
    )

## API to Re-Generate Note from LLM
@router.post("/{notes_id}/regenerate")
def regenerate_note_api(
    notes_id: int,
    db: Session = Depends(get_db)
):

    print("<!---- Regenerating Note ----!>")

    return regenerate_note(
        db=db,
        note_id=notes_id
    )


### API to Generate Notes directly from Cleaned documents via pipeline
from ..models.job import JobModel

from ..schemas.note import (
    GenerateDocumentNoteRequest
)

from ..tasks.note_pipeline_tasks import (
    run_note_pipeline
)

@router.post("/generate-via-document")
def generate_notes(
    payload: GenerateDocumentNoteRequest,
    db: Session = Depends(get_db)
):

    job = JobModel(
        filename=f"document_{payload.document_id}",
        status="queued",
        stage="notes"
    )

    db.add(job)

    db.commit()

    db.refresh(job)

    run_note_pipeline.delay(
        job.id,
        payload.document_id,
        payload.title,
        payload.chapter_id,
        payload.lesson_id,
        payload.goal
    )

    return {
        "job_id": job.id,
        "status": "queued"
    }