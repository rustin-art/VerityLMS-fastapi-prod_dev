# tasks/learning_assets_pipeline_tasks.py

from celery import chord

from ..celery_app import celery_app

from ..database import SessionLocal

from ..models.job import JobModel
from ..models.note import NoteModel

from .assessment_tasks import (
    generate_assessment_task
)

from .homework_tasks import (
    generate_homework_task
)

from ..services.note_lookup_service import (
    get_note_by_id
)

from .callbacks import (
    learning_assets_completed_callback,
    learning_assets_failed
)


@celery_app.task(
    name="src.tasks.learning_assets_pipeline_tasks.run_learning_assets_pipeline"
)
def run_learning_assets_pipeline(
    job_id: int,
    note_id: int
):
    """
    Orchestrator Task

    This task ONLY launches parallel tasks.

    It does not perform LLM generation itself.
    """

    db = SessionLocal()

    try:

        job = (
            db.query(JobModel)
            .filter(JobModel.id == job_id)
            .first()
        )

        if not job:
            raise ValueError(
                f"Job {job_id} not found"
            )
        ###################################
        ## Fetching via note lookup service
        ##
        ###################################

        note = get_note_by_id(
            db,
            note_id
        )

        if not note:
            raise ValueError(
                f"Note {note_id} not found"
            )

        job.status = "processing"

        job.stage = "launching_parallel_tasks"

        db.commit()

        # ---------------------------------------------------
        # Chord:
        #
        # assessment task
        # homework task
        #
        # THEN callback
        # ---------------------------------------------------

        workflow = chord(
            [
                generate_assessment_task.s(note_id),
                generate_homework_task.s(note_id)
            ]
        )

        callback = learning_assets_completed_callback.s(
            job_id,
            note_id
        )

        callback.link_error(
            learning_assets_failed.s(job_id)
        )

        workflow(callback)

        

        return {
            "workflow_id": workflow.id
        }

    finally:

        db.close()