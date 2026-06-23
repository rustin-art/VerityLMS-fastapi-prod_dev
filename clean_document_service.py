import logging

from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from ..models.cleaned_document import CleanedDocumentModel

logger = logging.getLogger(__name__)


def save_clean_document(
    db: Session,
    document_id: int,
    document_name: str,
    extraction_type: str,
    cleaned_text: str
) -> CleanedDocumentModel:
    """
    Idempotent upsert for cleaned documents.

    Safe for:
    - Celery retries
    - pipeline re-runs
    - partial failures
    """

    if not document_id:
        raise ValueError("document_id is required")

    if not extraction_type:
        raise ValueError("extraction_type is required")

    try:

        existing = (
            db.query(CleanedDocumentModel)
            .filter(
                CleanedDocumentModel.document_id == document_id,
                CleanedDocumentModel.extraction_type == extraction_type
            )
            .first()
        )

        # ------------------------------------
        # UPDATE EXISTING RECORD
        # ------------------------------------
        if existing:

            existing.document_name = document_name
            existing.cleaned_text = cleaned_text
            existing.status = "completed"

            db.commit()
            db.refresh(existing)

            logger.info(
                "Updated cleaned document "
                "document_id=%s extraction_type=%s",
                document_id,
                extraction_type
            )

            return existing

        # ------------------------------------
        # INSERT NEW RECORD
        # ------------------------------------
        cleaned_doc = CleanedDocumentModel(
            document_id=document_id,
            document_name=document_name,
            extraction_type=extraction_type,
            cleaned_text=cleaned_text,
            status="completed"
        )

        db.add(cleaned_doc)

        db.commit()
        db.refresh(cleaned_doc)

        logger.info(
            "Created cleaned document "
            "id=%s document_id=%s extraction_type=%s",
            cleaned_doc.id,
            document_id,
            extraction_type
        )

        return cleaned_doc

    except SQLAlchemyError:

        db.rollback()

        logger.exception(
            "Database error while saving cleaned document "
            "document_id=%s extraction_type=%s",
            document_id,
            extraction_type
        )

        raise

    except Exception as e:

        db.rollback()

        logger.exception(
            "Unexpected error while saving cleaned document "
            "document_id=%s extraction_type=%s",
            document_id,
            extraction_type,
            str(e),
        )

        raise

    except IntegrityError:

        db.rollback()

        existing = (
            db.query(CleanedDocumentModel)
            .filter(
                CleanedDocumentModel.document_id == document_id,
                CleanedDocumentModel.extraction_type == extraction_type,
            )
            .first()
        )

        if existing:
            return existing

        raise