from sqlalchemy.orm import Session
from typing import Any

from ..models.extracted_document import ExtractedDocumentModel


def save_extracted_document(
    db,
    filename,
    extraction_type,
    extracted_data
):
    try:
        print("Creating document")

        document = ExtractedDocumentModel(
            filename=filename,
            extraction_type=extraction_type,
            extracted_data=extracted_data
        )

        db.add(document)

        print("Committing...")
        db.commit()

        print("Refreshing...")
        db.refresh(document)

        print("Saved:", document.document_id)

        return document

    except Exception as e:
        import traceback

        print("SAVE DOCUMENT ERROR:", repr(e))
        traceback.print_exc()

        db.rollback()
        raise