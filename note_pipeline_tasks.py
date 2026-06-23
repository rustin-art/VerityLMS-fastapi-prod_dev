from ..celery_app import celery_app

from ..database import SessionLocal

from ..models.job import JobModel

from ..services.document_context_service import (
    get_document,
    build_document_context
)

from ..services.note_service import (
    generate_notes_from_document
)

from ..services.note_persistence_service import (
    save_note
)


@celery_app.task(
    name="src.tasks.note_pipeline_tasks.run_note_pipeline"
)
def run_note_pipeline(
    job_id,
    document_id,
    title,
    chapter_id,
    lesson_id,
    goal
):

    db = SessionLocal()

    try:

        job = db.query(JobModel).filter(
            JobModel.id == job_id
        ).first()

        job.status = "processing"
        print("<!---- Processsing ..... ----!>")
        job.stage = "loading_document"
        print("<!---- Loading Document ..... ----!>")

        db.commit()

        document = get_document(
            db,
            document_id
        )
        print("<!---- Building Context ..... ----!>")
        job.stage = "building_context"

        db.commit()

        context = build_document_context(
            document.cleaned_text
        )

        job.stage = "generating_notes"
        print("<!---- Generating Notes ..... ----!>")

        db.commit()

        result = generate_notes_from_document(
            goal,
            context
        )

        job.stage = "saving"
        print("<!---- Saving to Database ----!>")
        db.commit()

        note = save_note(
            db=db,
            document_id=document_id,
            title=title,
            chapter_id=chapter_id,
            lesson_id=lesson_id,
            goal=goal,
            content=result["content"],
            prompt=result["prompt"]
        )

        job.status = "completed"

        job.stage = "done"
        print("<!---- Completed ----!>")

        job.result = {
            "note_id": note.id
        }

        db.commit()

        return job.result

    except Exception as e:

        job.status = "failed"

        job.result = {
            "error": str(e)
        }

        db.commit()

        raise

    finally:

        db.close()