from datetime import datetime

from pydantic import BaseModel


class CleanedDocumentCreate(BaseModel):
    document_id: int
    document_name: str
    extraction_type: str
    cleaned_text: str


class CleanedDocumentResponse(
    CleanedDocumentCreate
):
    id: int
    status: str
    created_at: datetime | None = None

    class Config:
        from_attributes = True