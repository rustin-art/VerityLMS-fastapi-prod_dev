# services/document_context_service.py
import json

from fastapi import HTTPException

from ..models.cleaned_document import (
    CleanedDocumentModel
)


def get_document(db,document_id: int):
    """
    This Service is used for fetching extracted documents from model
    to pass to the generate_notes api
    Args:
    db : connect with db
    document_id: Key
    """
    document = db.query(
        CleanedDocumentModel
    ).filter(
        CleanedDocumentModel.document_id
        == document_id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document


def build_document_context(cleaned_text):
    """
    This Function is to prevent passing raw JSON to the model
    Helps in providing context to the LLM
    Args:
    extracted_data : context for LLM based on extracted_documents
    """
    if isinstance(cleaned_text, dict):

        return json.dumps(
            cleaned_text,
            indent=2,
            ensure_ascii=False
        )

    return str(cleaned_text)