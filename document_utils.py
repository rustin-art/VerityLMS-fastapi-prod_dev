# utils/document_utils.py

import logging

logger = logging.getLogger(__name__)


def get_extracted_document_id(doc):
    """
    Safely extracts document ID from DB model.
    Works for SQLAlchemy + response objects.
    """

    if not doc:
        raise ValueError("doc is None")

    # SQLAlchemy model (correct case)
    doc_id = getattr(doc, "document_id", None)

    # fallback (if future schema changes)
    if not doc_id:
        doc_id = getattr(doc, "id", None)

    if not doc_id:
        raise ValueError("Missing extracted document id (checked document_id and id)")

    return doc_id