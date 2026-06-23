# schemas/learning_assets.py

from pydantic import BaseModel


class GenerateLearningAssetsRequest(BaseModel):
    """
    Generate assessment + homework
    from an existing Note.

    Triggered after notes are already generated.
    """

    note_id: int


class LearningAssetsResponse(BaseModel):
    """
    Response returned immediately after
    queueing the Celery workflow.
    """

    job_id: int

    status: str

    note_id: int