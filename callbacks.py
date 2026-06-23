# tasks/callbacks.py

from ..celery_app import celery_app

from ..database import SessionLocal

from ..models.job import JobModel


@celery_app.task(
    name="src.tasks.callbacks.learning_assets_completed_callback"
)
def learning_assets_completed_callback(
    results,
    job_id: int,
    note_id: int
):
    """
    Called ONLY when every task in the chord succeeds.
    """

    db = SessionLocal()

    try:

        assessment_id = None
        homework_id = None

        for item in results:

            if item["type"] == "assessment":
                assessment_id = item["assessment_id"]

            elif item["type"] == "homework":
                homework_id = item["homework_id"]

        job = (
            db.query(JobModel)
            .filter(JobModel.id == job_id)
            .first()
        )

        job.status = "completed"

        job.stage = "done"

        job.result = {
            "note_id": note_id,
            "assessment_id": assessment_id,
            "homework_id": homework_id
        }

        db.commit()

        return job.result

    finally:

        db.close()


## Error Callback if either Homework/ Assessment Fails

@celery_app.task
def learning_assets_failed(
    request,
    exc,
    traceback,
    job_id
):
    db = SessionLocal()

    try:

        job = (
            db.query(JobModel)
            .filter(JobModel.id == job_id)
            .first()
        )

        job.status = "failed"

        job.result = {
            "error": str(exc)
        }

        db.commit()

    finally:
        db.close()