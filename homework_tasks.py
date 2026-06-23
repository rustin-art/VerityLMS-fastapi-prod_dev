# tasks/homework_tasks.py

from ..celery_app import celery_app

from ..database import SessionLocal

from ..models.note import NoteModel

from ..services.homework_service import (
    generate_homework_from_notes
)

from ..services.note_lookup_service import (
    get_note_by_id
)

from ..services.homework_persistence_service import (
    save_homework
)


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_kwargs={"max_retries": 3},
    name="src.tasks.homework_tasks.generate_homework_task"
)
def generate_homework_task(
    self,
    note_id: int
):
    """
    Generates homework from note.

    Runs independently.

    Returns homework_id for chord callback.
    """

    db = SessionLocal()

    try:

        note = get_note_by_id(
            db,
            note_id
        )

        result = generate_homework_from_notes(
            note.content
        )

        homework = save_homework(
            db=db,
            note_id=note.id,
            title=f"{note.title} Homework",
            chapter_id=note.chapter_id,
            lesson_id=note.lesson_id,
            homework_questions=result["questions"],
            prompt=result["prompt"]
        )

        return {
            "type": "homework",
            "homework_id": homework.id
        }

    finally:

        db.close()