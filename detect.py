from fastapi import APIRouter, File, UploadFile, Request, Depends
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.orm import Session

from ..services.file_service import save_upload
from ..services.document_service import save_extracted_document
from ..services.det_service import (
    run_det,
    )

from ..database import get_db

router = APIRouter(prefix="/detect", tags=["Detection"])



@router.post("")
async def detect(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    path = await save_upload(file)

    output = await run_in_threadpool(
        run_det,
        path
    )


    doc = save_extracted_document(
        db=db,
        filename=file.filename,
        extraction_type="det",
        extracted_data=output
    )

    return {
        "document_id": doc.document_id,
        "task": "det",
        "results": output
    }