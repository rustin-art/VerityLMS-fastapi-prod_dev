from sqlalchemy.orm import Session
from .document_service import save_extracted_document

## this function will post-process text before pushing to DB
def write_extracted_document(
    db: Session,
    filename: str,
    extraction_type: str,
    data: dict
):
    return save_extracted_document(
        db=db,
        filename=filename,
        extraction_type=extraction_type,
        extracted_data=data
    )