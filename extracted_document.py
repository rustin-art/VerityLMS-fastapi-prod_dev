from pydantic import BaseModel
from typing import Dict, Any, List


class ExtractedDocumentCreate(BaseModel):
    filename: str
    extraction_type: str
    extracted_data: Any


class ExtractedDocumentResponse(
    ExtractedDocumentCreate
):
    document_id: int

    class Config:
        from_attributes = True