from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.job import JobModel

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get("/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):

    job = db.query(JobModel).get(job_id)

    if not job:
        return {"error": "not found"}

    return {
        "job_id": job.id,
        "status": job.status,
        "stage": job.stage,
        "result": job.result
    }