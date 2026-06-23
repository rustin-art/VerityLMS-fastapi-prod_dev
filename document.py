from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.file_service import save_upload
from ..models.job import JobModel
from ..tasks.pipeline_tasks import run_extract_pipeline

router = APIRouter(prefix="/document", tags=["Document"])


@router.post("")
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):

    path = await save_upload(file)

    job = JobModel(
        filename=file.filename,
        status="queued",
        stage="det"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    run_extract_pipeline.delay(job.id, path, file.filename)

    return {"job_id": job.id, "status": "queued"}  