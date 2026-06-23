from pathlib import Path
import logging

from ..services.clean_document_service import save_clean_document
from ..services.document_cleaning_service import build_clean_text

from ..celery_app import celery_app
from ..database import SessionLocal

from ..models.job import JobModel

from ..services.pdf_service import pdf_to_images
from ..services.ocr_service import run_ocr
from ..services.unirec_service import run_unirec
from ..services.document_service import save_extracted_document

from ..utils.json_safe import make_json_safe
from ..utils.document_utils import get_extracted_document_id

logger = logging.getLogger(__name__)

# =====================================================
# PIPELINE A
# Image/PDF -> DET -> OCR -> Save Extracted Document
# =====================================================
#
# Flow:
#
# Upload File
#      ↓
# Redis Queue
#      ↓
# Celery Worker
#      ↓
# PDF ? -> Convert to Images
#      ↓
# Detection
#      ↓
# OCR Recognition
#      ↓
# Save extracted_document
#      ↓
# Update Job Status
#
# =====================================================

@celery_app.task(
    name="src.tasks.pipeline_tasks.run_extract_pipeline"
)
def run_extract_pipeline(
    job_id: int,
    file_path: str,
    filename: str
):
    """
    OCR Extraction Pipeline

    Flow:

    Upload
      ↓
    Create Job
      ↓
    Celery Worker
      ↓
    PDF → Images
      ↓
    OCR
      ↓
    Save extracted_document
      ↓
    Build cleaned text
      ↓
    Save cleaned_document
      ↓
    Update Job
    """

    db = SessionLocal()

    job = None

    try:

        # --------------------------------------------------
        # Load Job
        # --------------------------------------------------
        job = (
            db.query(JobModel)
            .filter(JobModel.id == job_id)
            .first()
        )

        if not job:
            raise ValueError(
                f"Job {job_id} not found"
            )

        # --------------------------------------------------
        # Mark Running
        # --------------------------------------------------
        job.status = "processing"
        job.stage = "ocr"

        db.commit()

        logger.info(
            "Starting OCR pipeline job_id=%s",
            job_id
        )

        # --------------------------------------------------
        # Determine Input Type
        # --------------------------------------------------
        ext = Path(filename).suffix.lower()

        if ext == ".pdf":

            pages = pdf_to_images(file_path)

            if not pages:
                raise ValueError(
                    "PDF conversion failed. No pages extracted."
                )

        else:

            pages = [file_path]

        logger.info(
            "Pages to process: %s",
            len(pages)
        )

        # --------------------------------------------------
        # OCR Processing
        # --------------------------------------------------
        results = []

        for page_number, page in enumerate(
            pages,
            start=1
        ):

            if not page:
                continue

            logger.info(
                "Processing OCR page=%s",
                page_number
            )

            page_result = run_ocr(page)

            logger.info(
                "OCR blocks found=%s page=%s",
                len(page_result),
                page_number
            )

            results.append(page_result)

        # --------------------------------------------------
        # Validate OCR Result
        # --------------------------------------------------
        if not results:
            raise ValueError(
                "OCR produced no text"
            )

        # --------------------------------------------------
        # Saving Extracted Document
        # --------------------------------------------------
        job.stage = "saving"
        db.commit()

        extracted_payload = {
            "pages": results
        }

        doc = save_extracted_document(
            db=db,
            filename=filename,
            extraction_type="ocr",
            extracted_data=make_json_safe(
                extracted_payload
            )
        )

        extracted_document_id = (
            get_extracted_document_id(doc)
        )

        logger.info(
            "Extracted document saved "
            "document_id=%s",
            extracted_document_id
        )

        # --------------------------------------------------
        # Build Clean Text
        # --------------------------------------------------
        cleaned_text = build_clean_text(
            extraction_type="ocr",
            extracted_data={
                "pages": results
            }
        )

        logger.info(
            "Clean text length=%s",
            len(cleaned_text)
        )

        # --------------------------------------------------
        # Save Cleaned Document
        # --------------------------------------------------
        cleaned_doc = save_clean_document(
            db=db,
            document_id=extracted_document_id,
            document_name=filename,
            extraction_type="ocr",
            cleaned_text=cleaned_text
        )

        logger.info(
            "Cleaned document saved "
            "id=%s document_id=%s",
            cleaned_doc.id,
            extracted_document_id
        )

        # --------------------------------------------------
        # Job Success
        # --------------------------------------------------
        job.status = "completed"
        job.stage = "done"

        job.result = {
            "document_id": extracted_document_id,
            "cleaned_document_id": cleaned_doc.id
        }

        db.commit()

        logger.info(
            "OCR pipeline completed "
            "job_id=%s document_id=%s",
            job_id,
            extracted_document_id
        )

        return job.result

    except Exception as e:

        logger.exception(
            "OCR pipeline failed job_id=%s",
            job_id
        )

        db.rollback()

        # ----------------------------------------------
        # Job Failure
        # ----------------------------------------------
        if job:

            try:

                job.status = "failed"
                job.stage = "error"

                job.result = {
                    "error": str(e)
                }

                db.commit()

            except Exception:

                db.rollback()

        raise

    finally:

        db.close()


# =====================================================
# PIPELINE B
# Image/PDF -> UniRec -> Save Extracted Document
# =====================================================
#
# Flow:
#
# Upload File
#      ↓
# Redis Queue
#      ↓
# Celery Worker
#      ↓
# UniRec Model
#      ↓
# Save extracted_document
#      ↓
# Update Job Status
#
# =====================================================

@celery_app.task(
    name="src.tasks.pipeline_tasks.run_unirec_pipeline"
)
def run_unirec_pipeline(
    job_id: int,
    file_path: str,
    filename: str
):
    """
    UniRec extraction pipeline.

    Used for:
    - Structured document understanding
    - Key-value extraction
    - Layout-aware extraction

    Produces:
    extracted_documents record
    """

    db = SessionLocal()

    try:

        # Fetch queued job
        job = db.query(JobModel).filter(JobModel.id == job_id).first()

        if not job:
            raise ValueError(
                f"Job {job_id} not found"
            )

        # Mark running
        job.status = "processing"
        job.stage = "unirec"

        db.commit()

        # =====================
        # UNIREC INFERENCE
        # =====================
        result = run_unirec(file_path)

        # Saving stage
        job.stage = "saving"
        db.commit()

        doc = save_extracted_document(
            db=db,
            filename=filename,
            extraction_type="unirec",
            extracted_data=result
        )

        # =====================================================
        # VALIDATION + NORMALIZATION
        # =====================================================

        logger.info("DOC OBJECT: %s", dir(doc))
        logger.info("DOC ATTRS: id=%s document_id=%s",
            getattr(doc, "id", None),
            getattr(doc, "document_id", None))

        # -----------------------------------------------------
        # Normalize extracted document ID (CRITICAL FIX)
        # -----------------------------------------------------

        extracted_document_id = get_extracted_document_id(doc)

        logger.info(
            "Extracted document saved: document_id=%s",
            extracted_document_id
        )

        # =====================================================
        # CLEANING STEP
        # =====================================================

        from ..services.document_cleaning_service import build_clean_text
        from ..services.clean_document_service import save_clean_document

        logger.info(
            "UNIREC RESULT TYPE: %s",
            type(result)
        )

        logger.info(
            "UNIREC RESULT PREVIEW: %s",
            str(result)[:2000]
        )

        cleaned_text = build_clean_text(
            extraction_type="unirec",
            extracted_data=result
        )

        # -----------------------------------------------------
        # Save cleaned document
        # -----------------------------------------------------

        cleaned_doc = save_clean_document(
            db=db,
            document_id=extracted_document_id,
            document_name=filename,
            extraction_type="unirec",
            cleaned_text=cleaned_text
        )

        # -----------------------------------------------------
        # Logging (use normalized ID)
        # -----------------------------------------------------
        logger.info(
            "Cleaned document saved: id=%s document_id=%s",
            cleaned_doc.id,
            extracted_document_id
        )

        # -------------------------
        # JOB COMPLETE
        # -------------------------

        # Mark complete
        job.status = "completed"
        job.stage = "done"

        job.result = {
            "document_id": doc.document_id
        }

        db.commit()

        return job.result

    except Exception as e:

        db.rollback()
        
        job.status = "failed"

        job.result = {
            "error": str(e)
        }

        db.commit()

        raise

    finally:

        db.close()