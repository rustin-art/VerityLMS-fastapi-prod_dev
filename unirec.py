from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..services.file_service import save_upload
from ..models.job import JobModel
from ..tasks.pipeline_tasks import run_unirec_pipeline

router = APIRouter(prefix="/unirec", tags=["UniRec"])

  
@router.post("")
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):

    path = await save_upload(file)

    job = JobModel(
        filename=file.filename,
        status="queued",
        stage="unirec"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    run_unirec_pipeline.delay(job.id, path, file.filename)

    return {"job_id": job.id, "status": "queued"}