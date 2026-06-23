from sqlalchemy.orm import Session

from ..models.cleaned_document import (
    CleanedDocumentModel
)


def get_clean_document(
    db: Session,
    document_id: int,
    extraction_type: str | None = None
):
    """
    Get a single cleaned document.
    """

    query = (
        db.query(CleanedDocumentModel)
        .filter(
            CleanedDocumentModel.document_id == document_id
        )
    )

    if extraction_type:
        query = query.filter(
            CleanedDocumentModel.extraction_type == extraction_type
        )

    return query.first()


def get_clean_documents(
    db: Session,
    skip: int = 0,
    limit: int = 100
):
    """
    List cleaned documents.
    """

    return (
        db.query(CleanedDocumentModel)
        .order_by(
            CleanedDocumentModel.created_at.desc()
        )
        .offset(skip)
        .limit(limit)
        .all()
    )