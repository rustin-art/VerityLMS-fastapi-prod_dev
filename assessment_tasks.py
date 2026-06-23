# tasks/assessment_tasks.py

from ..celery_app import celery_app

from ..database import SessionLocal

from ..models.note import NoteModel

from ..services.assessment_service import (
    generate_assessment_from_notes
)

from ..services.note_lookup_service import (
    get_note_by_id
)

from ..services.assessment_persistence_service import (
    save_assessment
)


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
    name="src.tasks.assessment_tasks.generate_assessment_task"
)
def generate_assessment_task(
    self,
    note_id: int
):
    """
    Generates assessment from note.

    Runs independently.

    Returns assessment_id for chord callback.
    """

    db = SessionLocal()

    try:

        note = get_note_by_id(
            db,
            note_id
        )

        result = generate_assessment_from_notes(
            note.content
        )

        assessment = save_assessment(
            db=db,
            note_id=note.id,
            title=f"{note.title} Assessment",
            chapter_id=note.chapter_id,
            lesson_id=note.lesson_id,
            mcq_pool=result["mcq_pool"],
            answers_pool=result["answers_pool"],
            prompt=result["prompt"]
        )

        return {
            "type": "assessment",
            "assessment_id": assessment.id
        }

    finally:

        db.close()