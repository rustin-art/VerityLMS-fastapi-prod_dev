from pathlib import Path

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from ..database import get_db
from ..models.job import JobModel
from ..services.file_service import save_upload
from ..tasks.pipeline_tasks import run_extract_pipeline

router = APIRouter(
    prefix="/ocr",
    tags=["OCR"]
)

SUPPORTED = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".pdf"
}


@router.post("")
async def upload_ocr(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    ext = Path(file.filename).suffix.lower()

    if ext not in SUPPORTED:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type"
        )

    path = await save_upload(file)

    # -------------------------------------------------
    # Create Job
    # -------------------------------------------------
    job = JobModel(
        filename=file.filename,
        status="queued",
        stage="ocr"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    # -------------------------------------------------
    # Queue OCR Pipeline
    # -------------------------------------------------
    run_extract_pipeline.delay(
        job.id,
        path,
        file.filename
    )

    return {
        "job_id": job.id,
        "status": "queued"
    }