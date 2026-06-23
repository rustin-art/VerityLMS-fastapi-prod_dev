from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas.extracted_document import (
    ExtractedDocumentCreate,
    ExtractedDocumentResponse
)
from ..services.document_service import save_extracted_document
from ..models.extracted_document import ExtractedDocumentModel


router = APIRouter(
    prefix="/extracted-documents",
    tags=["Extracted Documents"]
)

# -----------------------------------
# CREATE extracted document
# -----------------------------------
@router.post(
    "/create",
    response_model=ExtractedDocumentResponse
)
def create_extracted_document(
    payload: ExtractedDocumentCreate,
    db: Session = Depends(get_db)
):

    document = save_extracted_document(
        db=db,
        filename=payload.filename,
        extraction_type=payload.extraction_type,
        extracted_data=payload.extracted_data
    )

    return document


# -----------------------------------
# GET all documents
# -----------------------------------
@router.get(
    "/all",
    response_model=List[ExtractedDocumentResponse]
)
def get_all_documents(
    db: Session = Depends(get_db)
):

    return db.query(ExtractedDocumentModel).all()


# -----------------------------------
# GET single document by ID
# -----------------------------------
@router.get(
    "/{document_id}",
    response_model=ExtractedDocumentResponse
)
def get_document(
    document_id: int,
    db: Session = Depends(get_db)
):

    document = db.query(ExtractedDocumentModel).filter(
        ExtractedDocumentModel.document_id == document_id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    return document


# -----------------------------------
# DELETE document
# -----------------------------------
@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db)
):

    document = db.query(ExtractedDocumentModel).filter(
        ExtractedDocumentModel.document_id == document_id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    db.delete(document)
    db.commit()

    return {
        "message": "Document deleted successfully",
        "document_id": document_id
    }